import requests
from http.cookies import SimpleCookie
from requests.cookies import RequestsCookieJar

from bs4 import BeautifulSoup
from typing import Optional

from constants import AOTY_PUBLICATION_URL, AOTY_REQUEST_HEADERS
from src.collector.entities.publication_review import PublicationReview


def get_reviews(publication_name) -> [PublicationReview]:

    # TODO: reuse session between requests, perhaps with an object

    formatted_uri = AOTY_PUBLICATION_URL.format(publication_name=publication_name)

    # cookies = SimpleCookie()
    # cookies.load('FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CP-cxIAP-cxIAEsACCENA0EgAAAAAEPgACiQAAATUYDyFyIgmDD4NCuAyZoUQogrSAgxIBAACgDBoAAkHQkaRABoEBgABEEAEgQMgAJQOAAQAIAABAICIECgQAIRACIAIAAQGIAAQCIAEACAECAAAAQBgZCAAADAMQIQAgzgACYgAYIsJkAkQAFBCACEEAAAAEgFQYAMICEkAIhAYAQyIiViQQAAQECAAAABCAeAARKUKAYQAAIGQRAgAA.YAAAD_gAAAA%22%2C%222~~dv.41.55.89.108.117.149.192.211.228.259.311.313.358.397.415.424.445.449.469.486.491.494.495.540.559.609.621.737.803.899.904.979.981.1029.1031.1092.1097.1126.1186.1205.1215.1225.1270.1301.1307.1415.1419.1423.1525.1558.1579.1591.1598.1638.1697.1712.1735.1753.1782.1786.1808.1832.1842.1866.1911.1944.1958.1985.2010.2052.2056.2074.2088.2133.2137.2145.2183.2220.2312.2316.2322.2328.2343.2358.2373.2400.2411.2415.2425.2427.2461.2465.2481.2499.2510.2517.2527.2535.2542.2559.2569.2571.2572.2577.2595.2602.2628.2642.2650.2651.2652.2656.2669.2677.2684.2687.2690.2695.2729.2767.2768.2770.2787.2798.2805.2814.2816.2822.2839.2844.2854.2867.2872.2874.2878.2887.2898.2919.2920.2922.2949.2950.2964.2970.3002.3005.3010.3012.3017.3025.3055.3070.3089.3109.3126.3128.3130.3155.3163.3172.3189.3194.3198.3213.3230.3234.3244.3251.3253.3254.3290.3292.3299.3330.3331.4131.4531.7235.9731%22%2C%22D032DE40-773B-4175-8C8A-81C2275CF412%22%5D%5D; '
    #              'Path=/; '
    #              'Expires=05-06-2025 9:52:33.000Z UTC; '
    #              'Domain=.albumoftheyear.org; '
    #              'Size=1225; '
    #              'Priority=Medium; ')
    # jar = RequestsCookieJar()
    # jar.update(cookies)

    # Cookie(version, name, value, port, port_specified, domain,
    # domain_specified, domain_initial_dot, path, path_specified,
    # secure, discard, comment, comment_url, rest)
    cookie = RequestsCookieJar()
    cookie.set('FCCDCF',
               '%5Bnull%2Cnull%2Cnull%2C%5B%22CP-cxIAP-cxIAEsACCENA0EgAAAAAEPgACiQAAATUYDyFyIgmDD4NCuAyZoUQogrSAgxIBAACgDBoAAkHQkaRABoEBgABEEAEgQMgAJQOAAQAIAABAICIECgQAIRACIAIAAQGIAAQCIAEACAECAAAAQBgZCAAADAMQIQAgzgACYgAYIsJkAkQAFBCACEEAAAAEgFQYAMICEkAIhAYAQyIiViQQAAQECAAAABCAeAARKUKAYQAAIGQRAgAA.YAAAD_gAAAA%22%2C%222~~dv.41.55.89.108.117.149.192.211.228.259.311.313.358.397.415.424.445.449.469.486.491.494.495.540.559.609.621.737.803.899.904.979.981.1029.1031.1092.1097.1126.1186.1205.1215.1225.1270.1301.1307.1415.1419.1423.1525.1558.1579.1591.1598.1638.1697.1712.1735.1753.1782.1786.1808.1832.1842.1866.1911.1944.1958.1985.2010.2052.2056.2074.2088.2133.2137.2145.2183.2220.2312.2316.2322.2328.2343.2358.2373.2400.2411.2415.2425.2427.2461.2465.2481.2499.2510.2517.2527.2535.2542.2559.2569.2571.2572.2577.2595.2602.2628.2642.2650.2651.2652.2656.2669.2677.2684.2687.2690.2695.2729.2767.2768.2770.2787.2798.2805.2814.2816.2822.2839.2844.2854.2867.2872.2874.2878.2887.2898.2919.2920.2922.2949.2950.2964.2970.3002.3005.3010.3012.3017.3025.3055.3070.3089.3109.3126.3128.3130.3155.3163.3172.3189.3194.3198.3213.3230.3234.3244.3251.3253.3254.3290.3292.3299.3330.3331.4131.4531.7235.9731%22%2C%22D032DE40-773B-4175-8C8A-81C2275CF412%22%5D%5D',
               domain='albumoftheyear.org',
               path='/',
               # expires=None
               expires='Sat, 05-06-2025 9:52:33 UTC'
               )

    response = requests.get(formatted_uri, headers=AOTY_REQUEST_HEADERS, cookies=cookie)

    html = response.text
    reviews = extract_reviews(html, publication_name)

    return reviews


def extract_reviews(html, publication_name) -> [PublicationReview]:

    publication_reviews = []
    reviews_html = BeautifulSoup(html, 'html.parser')\
        .findAll('div', attrs={'class': 'albumBlock'})
    for review_html in reviews_html:
        review = extract_data(review_html, publication_name)

        if review:
            publication_reviews.append(review)

    return publication_reviews


def extract_data(review_html, publication_name) -> Optional[PublicationReview]:

    release_name = review_html.find('div', attrs={'class': 'albumTitle'}).text
    rating = review_html.find('div', attrs={'class': 'rating'})
    artist = review_html.find('div', attrs={'class': 'artistTitle'}).text

    if not rating:
        return None

    link = review_html.find('div', attrs={'class': 'ratingText'}).a['href']
    score = int(rating.text)

    return PublicationReview(
        artist=artist,
        release_name=release_name,
        score=score,
        link=link,
        publication_name=publication_name
    )


if __name__ == "__main__":
    reviews = get_reviews('57-the-needle-drop')
    print(reviews)
