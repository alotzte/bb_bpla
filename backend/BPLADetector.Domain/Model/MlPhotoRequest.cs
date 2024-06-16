using System.Text.Json.Serialization;

namespace BPLADetector.Domain.Model;

public class MlPhotoRequest
{
    [JsonPropertyName("photos")] public MlPhotoRequestItem[] Photos { get; set; }
}

public class MlPhotoRequestItem
{
    [JsonPropertyName("url")] public string Url { get; set; }
    [JsonPropertyName("correlation_id")] public Guid CorrelationId { get; set; }
}