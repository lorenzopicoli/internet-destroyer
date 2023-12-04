import json
import requests
import re
import config
import utils
import os


def api_base_url():
    return f'https://public-api.wordpress.com/rest/v1.1/sites/{config.blog_url}'


API_KEY = os.environ['WORDPRESS_API_KEY']
base_headers = {
    'Authorization': f'Bearer {API_KEY}',
}


def markdown_to_html(md_text):
    # Replace Markdown headers with HTML headers
    md_text = re.sub(r'#{6}\s?(.*?)\n', r'<h6>\1</h6>', md_text)  # h6
    md_text = re.sub(r'#{5}\s?(.*?)\n', r'<h5>\1</h5>', md_text)  # h5
    md_text = re.sub(r'#{4}\s?(.*?)\n', r'<h4>\1</h4>', md_text)  # h4
    md_text = re.sub(r'#{3}\s?(.*?)\n', r'<h3>\1</h3>', md_text)  # h3
    md_text = re.sub(r'#{2}\s?(.*?)\n', r'<h2>\1</h2>', md_text)  # h2
    md_text = re.sub(r'#{1}\s?(.*?)\n', r'<h1>\1</h1>', md_text)  # h1

    # Replace bold and italic
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md_text)  # bold
    md_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>',
                     md_text)             # italic

    # Replace Markdown links with HTML links
    md_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md_text)

    return md_text


def slugify(title):
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug


def post_to_wordpress(title, content, image_id, tags):
    print(f"Posting to wordpress: {title}, {image_id}")

    if config.dry_run:
        print("Dry run mode is enabled. Returning mock response from wordpress.")
        return "https://my-blog.com/2021/08/01/this-is-a-test-post/"

    endpoint = f"{api_base_url()}/posts/new"
    data = {
        "title": title,
        "content": markdown_to_html(content),
        "slug": slugify(title),
        "tags": tags,
        "author": config.author,
        "featured_image": f"{image_id}"
    }

    json_data = json.dumps(data)

    headers = {
        **base_headers,
        'Content-Type': 'application/json'
    }

    response = requests.post(endpoint, data=json_data, headers=headers)

    if response.status_code == 200:
        r_json = response.json()
        utils.print_verbose(
            f"Successfully posted to wordpress: {r_json['URL']}")
        return r_json["URL"]
    else:
        print("Error while posting to wordpress:",
              response.status_code, response.text)
    return ""


def upload_image(image_path: str, alt: str):
    utils.print_verbose(f"Uploading image {image_path} to wordpress")

    if config.dry_run:
        print("Dry run mode is enabled. Returning mock response from wordpress.")
        return "https://myblog.com/wp-content/uploads/2021/08/1-1.jpg", 1

    if image_path is None:
        return "", ""

    endpoint = f"{api_base_url()}/media/new"
    file = {
        'media[]': open(image_path, 'rb'),
    }
    # Wordpress seems to simply ignore this even though its in their docs?
    # files['attrs[0][alt]'] = urllib.parse.quote_plus(alt)

    response = requests.post(
        endpoint, headers=base_headers, files=file)

    if response.status_code == 200:
        uploaded_url = response.json().get('media')[0].get('URL')
        id = response.json().get('media')[0].get('ID')
        print(
            f"Successfully uploaded {response.json().get('media')[0].get('URL')} to wordpress")

        return uploaded_url, id
