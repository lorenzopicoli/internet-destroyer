import prompts
import random
import config
import llm_api
from image import Image
import utils


class Article:
    def __init__(self, idea: str, title: str, images: [Image]):
        self.title = title
        self.idea = idea
        self.images = images
        self.sections = []
        self.keywords = []
        self.hook = ""

    def get_title(self):
        return self.title

    def get_sections(self):
        return self.sections

    def format_image(self, link: str, alt: str):
        return f'<img width="100%" height="100%" src="{link}" alt="{alt}" title="{alt}" loading="lazy" />'

    def generate_section(self):
        utils.print_verbose(
            f"Generating sections for title: {self.title} and idea: {self.idea}")
        sections = llm_api.call_llm(
            self.title, prompts.generate_sections_prompt())
        self.sections = sections

    def generate_section_content(self, section: str):
        utils.print_verbose(
            f"Generating content for section: {section} and title: {self.title}")
        content = llm_api.call_llm(
            f'The title is \"{self.title}\" and the section you are writing is \"{section}\"', prompts.section_content_prompt(), 1.3)
        return content

    def get_random_image(self):
        utils.print_verbose(
            f"Getting random image for title: {self.title}, images length: {len(self.images)}")
        if len(self.images) > 0:
            image = random.choice(self.images)
            return self.format_image(image.link, image.alt)
        return ""

    def generate_hook_paragraph(self):
        utils.print_verbose(
            f"Generating hook paragraph for title: {self.title} and idea: {self.idea}. Sections are: {self.sections}")
        sections = ', '.join(self.sections)
        hook = llm_api.call_llm(
            f'The title is \"{self.title}\" and the sections are: \"{sections}\"', prompts.hook_paragraph_prompt())
        self.hook = hook
        return hook

    def generate_keywords_and_sources(self, content: str):
        utils.print_verbose(
            f"Generating keywords and sources for title: {self.title} and idea: {self.idea}")
        keyword_and_sources = llm_api.call_llm(
            content, prompts.keywords_prompt())
        self.keywords = keyword_and_sources.get('keywords')
        return keyword_and_sources

    def get_featured_image_id(self):
        utils.print_verbose(
            f"Getting featured image for title: {self.title}, images length: {len(self.images)}")
        if len(self.images) > 0:
            return random.choice(self.images).id
        return ""

    def generate_content(self):
        print(f"Generating sections for title: {self.title}")
        self.generate_section()
        print(f"Generating hook paragraph for title: {self.title}")
        hook = self.generate_hook_paragraph()
        content = [hook]
        for section in self.sections:
            try:
                print(f"Appending image for section: {section}")
                image = self.get_random_image()
                print(f"Generating content for section: {section}")
                section_content = self.generate_section_content(section)
                content.append('\n\n<h2>' + section + '</h2>')
                content.append(image)
                content.append('\n' + section_content)
            except Exception as e:
                print(
                    f"Failed while generating section: {section}, for title {self.title} and idea {self.idea}. Error is {e}")

        # Is it really necessary to pass all the content to generate keywords? Maybe just the title and sections? Would save a lot of
        # tokens in the API calls
        utils.print_verbose(f"Content is: {content}")
        keywords = self.generate_keywords_and_sources('\n'.join(content))

        content.append('\nRelated content and sources:')
        for k in keywords.get('related'):
            content.append(k)

        content.append('\n\nPost keywords: ' +
                       ', '.join(keywords.get('keywords')))
        utils.print_verbose(
            f"Generated content for title: {self.title} and idea: {self.idea}:")
        utils.print_verbose('\n'.join(content))
        return '\n'.join(content)
