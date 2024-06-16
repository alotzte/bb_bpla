using System.Text.Json.Serialization;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedArchive;

public sealed class UploadProcessedArchiveRequestDto
{
    [JsonPropertyName("link")] public string Link { get; set; }
    [JsonPropertyName("txt")] public string Txt { get; set; }

    [JsonPropertyName("processed_milliseconds")]
    public long ProcessedMilliseconds { get; set; }
}