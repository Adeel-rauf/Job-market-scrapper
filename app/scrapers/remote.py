from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app.db import SessionLocal
from app.repository import get_or_create_company, upsert_job
from selenium.common.exceptions import TimeoutException, WebDriverException


@dataclass
class RemoteOKJob:
    title: str
    company: str
    location: str
    url: str



def make_driver() -> webdriver.Chrome:
    opts = Options()
    # opts.add_argument("--headless=new")

    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-extensions")

    opts.page_load_strategy = "eager" 

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(30) 
    driver.set_script_timeout(30)
    return driver




def load_more(driver, target_jobs: int = 400, max_rounds: int = 40) -> int:
    
    wait = WebDriverWait(driver, 15)

    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.job")))

    last_count = 0
    stagnant_rounds = 0

    for i in range(max_rounds):
        # Count current jobs
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        count = len(soup.select("tr.job[data-id]"))

        print(f"[load_more] round={i+1} jobs={count} stagnant={stagnant_rounds}")

        if count >= target_jobs:
            return count

        if count > last_count:
            last_count = count
            stagnant_rounds = 0
        else:
            stagnant_rounds += 1
            
            if stagnant_rounds >= 5:
                return count

        
        driver.execute_script("window.scrollBy(0, 1200);")
        time.sleep(1.2)

        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        
        try:
            btn = driver.find_element(By.CSS_SELECTOR, "button#load-more")
            if btn.is_displayed() and btn.is_enabled():
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(2.0)
        except Exception:
            pass

    return last_count



def get_with_retry(driver: webdriver.Chrome, url: str, retries: int = 3) -> None:
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            driver.get(url)
            return
        except (TimeoutException, WebDriverException) as e:
            last_err = e
            # stop loading and try again
            try:
                driver.execute_script("window.stop();")
            except Exception:
                pass
            time.sleep(2 * attempt)
    raise last_err

def parse_jobs(html: str) -> List[RemoteOKJob]:
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select("tr.job")

    jobs: List[RemoteOKJob] = []
    for r in rows:
        
        if r.get("data-id") is None:
            continue

        title_el = r.select_one("h2")
        company_el = r.select_one("h3")
        loc_el = r.select_one(".location")
        link_el = r.select_one("a.preventLink")

        if not (title_el and company_el and link_el):
            continue

        title = title_el.get_text(strip=True)
        company = company_el.get_text(strip=True)
        location = loc_el.get_text(strip=True) if loc_el else "Remote"
        url = "https://remoteok.com" + link_el.get("href", "").strip()

        jobs.append(RemoteOKJob(title=title, company=company, location=location, url=url))

    return jobs

def wait_until_jobs_settle(driver, css="tr.job", stable_rounds=3, sleep_s=1.0, max_wait_s=20):
    """
    Wait until the number of job rows stops increasing for `stable_rounds`.
    This avoids random counts due to async rendering.
    """
    start = time.time()
    last = 0
    stable = 0

    while time.time() - start < max_wait_s:
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        count = len(soup.select(css))

        if count > last:
            last = count
            stable = 0
        else:
            stable += 1
            if stable >= stable_rounds:
                return last

        time.sleep(sleep_s)

    return last

def run() -> None:
    driver = make_driver()
    try:
        get_with_retry(driver, "https://remoteok.com/", retries=3)

        time.sleep(2)

        loaded = load_more(driver, target_jobs=400, max_rounds=40)
        print("Loaded job rows =", loaded)

        final_count = wait_until_jobs_settle(driver, stable_rounds=3, sleep_s=1.2, max_wait_s=25)
        print("Settled job rows =", final_count)

        html = driver.page_source
        jobs = parse_jobs(html)
        print(f"Found {len(jobs)} jobs")

        created_jobs = 0
        with SessionLocal() as session:
            for j in jobs:
                company = get_or_create_company(session, name=j.company, location=None)
                created = upsert_job(
                    session,
                    title=j.title,
                    location=j.location,
                    company=company,
                    url=j.url,
                    description=None,
                )
                if created:
                    created_jobs += 1

            session.commit()

        print(f"Inserted {created_jobs} new jobs)")

    finally:
        driver.quit()



if __name__ == "__main__":
    run()
