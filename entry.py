class Entry(object):
    def __init__(self, name, summary, keywords, transcript, audio_file_url, tags, location):
        self.name = name
        self.summary = summary
        self.keywords = keywords
        self.transcript = transcript
        self.audio_file_url = audio_file_url
        self.tags = tags
        self.location = location

    @staticmethod
    def from_dict(source):
        return Entry(name=source.name, summary=source.summary, keywords=source.keywords, transcript=source.transcript, audio_file_url=source.audio_file_url, tags=source.tags, location=source.location)

    def to_dict(self):
        return {
            "name": self.name,
            "summary": self.summary,
            "keywords": self.keywords,
            "transcript": self.transcript,
            "audio_file_url": self.audio_file_url,
            "tags": self.tags,
            "location": self.location
        }

    def __repr__(self):
        return(
            u'Entry(name={}, summary={}, keywords={}, transcript={}, audio_file_url={}, tags={}, location={})'
            .format(self.name, self.summary, self.keywords, self.transcript, self.audio_file_url, self.tags, self.location))