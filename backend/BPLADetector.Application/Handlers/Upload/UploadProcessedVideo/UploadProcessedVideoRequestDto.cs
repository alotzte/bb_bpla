using System.Text.Json.Serialization;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedVideo;

public sealed class UploadProcessedVideoRequestDto
{
    [JsonPropertyName("link")] public string Link { get; set; }
    [JsonPropertyName("marks")] public float[]? Marks { get; set; }
    [JsonPropertyName("processed_milliseconds")]
    public long ProcessedMilliseconds { get; set; }
}