using BPLADetector.Application.DTO;

namespace BPLADetector.Infrastructure.Extensions;

public static class ModelExtensions
{
    public static UploadFileItem ToUploadFileItem(this IFormFile formFile)
    {
        return new UploadFileItem
        {
            Filename = formFile.FileName,
            Length = formFile.Length,
            Stream = formFile.OpenReadStream()
        };
    }
}