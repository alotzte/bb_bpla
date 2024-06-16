using BPLADetector.Domain.Model;

namespace BPLADetector.Application.Abstractions;

public interface IMlHttpClient
{
    Task<MlPhotosResponse?> UploadPhotosAsync(IEnumerable<MlPhotoRequestItem> items, CancellationToken cancellationToken = default);
    Task UploadVideosAsync(IEnumerable<string> urls, Guid correlationId, CancellationToken cancellationToken = default);
    Task UploadArchiveAsync(string url, Guid correlationId, CancellationToken cancellationToken = default);
}