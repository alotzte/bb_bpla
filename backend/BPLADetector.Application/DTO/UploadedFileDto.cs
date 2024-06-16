using BPLADetector.Domain.Enums;

namespace BPLADetector.Application.DTO;

public class UploadedFileDto
{
    public DateTime UploadDatetime { get; set; }
    public string Filename { get; set; } = null!;
    public string Uri { get; set; } = null!;
    public string OriginalPresignedUrl { get; set; } = null!;
    public FileType Type { get; set; }
    public UploadStatus Status { get; set; }
    public Guid CorrelationId { get; set; } = Guid.NewGuid();
}