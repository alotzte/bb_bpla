using BPLADetector.Domain.Enums;

namespace BPLADetector.Domain.Helpers;

public static class FileTypeHelper
{
    public static FileType GetFileType(string filename)
    {
        var extension = Path.GetExtension(filename).Replace(".", string.Empty);

        return extension switch
        {
            "jpg" or "png" or "psd" or "jpeg" => FileType.Image,
            "mp4" or "avi" or "mov" or "wmv" or "m4v" or "webm" => FileType.Video,
            "zip" => FileType.Archive,
            _ => throw new ArgumentOutOfRangeException()
        };
    }
}