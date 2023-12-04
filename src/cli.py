import llm_api
import wordpress
import prompts
from article import Article
import argparse
import config
from image import ImageDownloader


def main():
    parser = argparse.ArgumentParser(description="Internet Littering AI")

    parser.add_argument('--generate-alt', action='store_true',
                        help='Generate alt text for images. Requires calls to LLM API')
    parser.add_argument('--dry-run', action='store_true',
                        help='Enable dry run mode')
    parser.add_argument('--prompt', type=str, help='Specify a prompt string')
    parser.add_argument('--blog-url', type=str,
                        help='Specify the wordpress blog url')
    parser.add_argument('--author', type=str,
                        help='Specify the wordpress author')
    parser.add_argument('--keyword-count', type=int,
                        help='Number of keywords to generate')
    parser.add_argument('--idea-count', type=int,
                        help='Number of ideas to generate')
    parser.add_argument('--title-count', type=int,
                        help='Number of titles to generate')
    parser.add_argument('--section-count', type=int,
                        help='Number of sections to generate for each article')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose mode')

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run mode is enabled.")

    if args.prompt:
        print(f"Prompt is set to: {args.prompt}")

    if args.verbose:
        print("Verbose mode is enabled.")

    if args.generate_alt:
        print("Alt text for images is enabled.")

    if args.author:
        print(f"Author is set to: {args.author}")

    if args.blog_url:
        print(f"Blog url is set to: {args.blog_url}")

    if args.keyword_count:
        print(f"Keyword count is set to: {args.keyword_count}")

    if args.idea_count:
        print(f"Idea count is set to: {args.idea_count}")

    if args.section_count:
        print(f"Section count is set to: {args.section_count}")

    # Update the global variables in config.py
    config.dry_run = args.dry_run
    config.verbose = args.verbose
    config.blog_url = args.blog_url
    config.author = args.author
    config.keyword_count = args.keyword_count
    config.idea_count = args.idea_count
    config.section_count = args.section_count

    articles_created = []
    images_uploaded = []

    for subject in [args.prompt]:
        images = ImageDownloader(subject, "images", 15).download()
        if args.generate_alt:
            for image in images:
                image.generate_alt_text()

        print(f"Generated {len(images)} images")
        for image in images:
            image.upload()
            images_uploaded.append(image)

        print("\n\n")
        print(f"Generating titles for subject: {subject}")
        titles = llm_api.call_llm(
            subject, prompts.ideas_prompt(), temp=1.4)
        print(f"Generated {len(titles)} title(s)")
        for title in titles:
            print(f"Generating article for title: {title}")
            article = Article(subject, title, images)
            print(f"Generating content for title: {title}")
            content = article.generate_content()
            print(f"Getting featured media for article: {title}")
            featured_media = article.get_featured_image_id()
            tags = article.keywords
            final_url = wordpress.post_to_wordpress(
                title, content, featured_media, tags)
            print(f"Posted: {final_url}")
            articles_created.append(final_url)
            print("\n\n")

    print("===== SUMMARY =====")
    print(f"Created {len(articles_created)} articles")
    print(f"Articles:")
    for article in articles_created:
        print(f" - URL: {article}")
    print(f"Uploaded {len(images_uploaded)} images")
    print(f"Images:")
    for image in images_uploaded:
        print(
            f" - URL: {image.link}")
        print(f"   - Source: {image.source_link}")
        print(f"   - Filepath: {image.file_path}")


if __name__ == "__main__":
    main()
