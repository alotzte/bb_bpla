using BPLADetector.Application.DTO;
using UnidecodeSharpFork;

namespace BPLADetector.Infrastructure.Extensions;

public static class ModelExtensions
{
    public static UploadFileItem ToUploadFileItem(this IFormFile formFile)
    {
        return new UploadFileItem
        {
            Filename = formFile.FileName.Unidecode(),
            Length = formFile.Length,
            Stream = formFile.OpenReadStream()
        };
    }
}