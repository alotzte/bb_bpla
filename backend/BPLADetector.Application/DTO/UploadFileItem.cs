namespace BPLADetector.Application.DTO;

public class UploadFileItem
{
    public string Filename { get; set; }
    public long Length { get; set; }
    public Stream Stream { get; set; }
}