using BPLADetector.Application.Handlers.File.GetProcessedFile;
using BPLADetector.Application.Handlers.Results.GetProcessedFiles;
using BPLADetector.Domain.Model;

namespace BPLADetector.Application.Abstractions;

public interface IDomainRepository
{
    Task<UploadedFile?> GetUploadedFileByCorrelationId(
        Guid correlationId,
        CancellationToken cancellationToken = default);

    public Task<List<UploadedFile>> GetUploadedFilesByCorrelationId(
        IEnumerable<Guid> correlationIds,
        CancellationToken cancellationToken = default);

    Task<GetFilesPagedResponse> GetProcessedFiles(
        int limit,
        int offset,
        CancellationToken cancellationToken = default);

    Task<GetProcessedFileResponse?> GetProcessedFileByCorrelationId(Guid correlationId, CancellationToken cancellationToken = default);
    Task AddAsync<T>(T item, CancellationToken cancellationToken = default);
    void AddRange<T>(IEnumerable<T> items) where T : class, IDomainModel;
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}