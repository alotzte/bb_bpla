using BPLADetector.Application.DTO;
using BPLADetector.Domain.Model;

namespace BPLADetector.Application.Abstractions;

public interface IS3Service
{
    Task<List<UploadedFile>> PutObjectsAsync(IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default);
}