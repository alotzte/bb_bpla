using BPLADetector.Application.DTO;
using BPLADetector.Domain.Model;

namespace BPLADetector.Application.Abstractions;

public interface IS3Service
{
    Task<List<UploadedFileDto>> PutObjectsAsync(IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default);

    string TransformPresignedUrl(string presignedUrl);
}