using BPLADetector.Domain.Enums;

namespace BPLADetector.Domain.Model;

public class ProcessedFile
{
    public int Id { get; set; }
    public DateTime UploadDatetime { get; set; }
    public long? ProcessedMilliseconds { get; set; }
    public string Filename { get; set; } = null!;
    public string Uri { get; set; } = null!;
    public string? TxtUrl { get; set; }
    public FileType Type { get; set; }
    public float[]? Marks { get; set; }
    public Guid? CorrelationId { get; set; }

    public virtual UploadedFile? UploadedFile { get; set; }
}