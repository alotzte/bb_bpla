namespace BPLADetector.Application.DTO;

public class ProcessedFileItemDto
{
    public long Id { get; set; }
    public string Title { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Status { get; set; } = null!;
    public string? Txt { get; set; }
    public DateTime? UploadDateTime { get; set; }
    public long? ProcessedTime { get; set; }
}