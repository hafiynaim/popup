import re
from urllib.parse import urlparse

def extract_features(url):
    url_length = len(url)
    num_dots = url.count('.')
    has_https = 1 if 'https' in url else 0
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    suspicious_keywords = 1 if re.search(r'login|secure|bank|verify', url) else 0

    parsed_url = urlparse(url)
    domain_length = len(parsed_url.netloc)

    return [url_length, num_dots, has_https, has_ip, suspicious_keywords, domain_length]
