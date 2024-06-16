using BPLADetector.Application.DTO;

namespace BPLADetector.Application.Abstractions;

public interface IS3Service
{
    Task<List<UploadedFileDto>> PutObjectsAsync(IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default);
}