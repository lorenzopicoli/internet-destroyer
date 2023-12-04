import uuid
from thirdparty.downloader import download
import llm_api
import wordpress


class Image:
    def __init__(self, file_path: str,  source_link: str, original_query: str, alt: str = ""):
        self.file_path = file_path
        self.source_link = source_link
        self.original_query = original_query

        self.alt = alt
        self.id = None
        self.link = None

    def generate_alt_text(self):
        url = self.link if self.link else self.source_link
        alt = llm_api.call_vision(self.original_query, url)
        self.alt = alt

    def upload(self):
        uploaded_url, id, = wordpress.upload_image(self.file_path, self.alt)
        self.link = uploaded_url
        self.id = id


class ImageDownloader:
    def __init__(self, subject: str, out_dir: str, limit: int = 15):
        self.subject = subject
        self.out_dir = out_dir
        self.limit = limit

    def download(self) -> [Image]:
        random_uuid = str(uuid.uuid4())
        download_result = download(self.subject, limit=self.limit,  output_dir=self.out_dir + '/' + random_uuid,
                                   adult_filter_off=True, force_replace=True, timeout=60, verbose=True)
        images = []
        for result in download_result:
            images.append(Image(result.get('file_path'),
                          result.get('source'), self.subject))
        return images
