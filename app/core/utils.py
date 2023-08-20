# import magic
# import mimetypes
import secrets
import string


# def guessMime(file) -> str:
#     return magic.from_buffer(file, mime=True)
#
#
# def guessFileExtension(file) -> str:
#     mime = guessMime(file)
#     return mimetypes.guess_extension(mime)


def generate_file_name(length=5) -> string:
    filename = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length))
    return filename
