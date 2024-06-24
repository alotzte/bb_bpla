using BPLADetector.Application.Abstractions;
using BPLADetector.Application.DTO;
using BPLADetector.Application.Handlers.File.GetProcessedFile;
using BPLADetector.Application.Handlers.Results.GetProcessedFiles;
using BPLADetector.Domain.Model;
using Microsoft.EntityFrameworkCore;

namespace BPLADetector.Infrastructure.Database;

public class DomainRepository : IDomainRepository
{
    private readonly ILogger<DomainRepository> _logger;
    private readonly BplaContext _context;

    public DomainRepository(ILogger<DomainRepository> logger, BplaContext context)
    {
        _logger = logger;
        _context = context;
    }

    public Task<UploadedFile?> GetUploadedFileByCorrelationId(
        Guid correlationId,
        CancellationToken cancellationToken = default)
    {
        return _context.UploadedFiles
            .Where(uploadedFile => uploadedFile.CorrelationId == correlationId)
            .FirstOrDefaultAsync(cancellationToken);
    }

    public Task<List<UploadedFile>> GetUploadedFilesByCorrelationId(
        IEnumerable<Guid> correlationIds,
        CancellationToken cancellationToken = default)
    {
        return _context.UploadedFiles
            .Where(uploadedFile => correlationIds.Contains(uploadedFile.CorrelationId))
            .ToListAsync(cancellationToken);
    }

    public async Task<GetFilesPagedResponse> GetProcessedFiles(
        int limit,
        int offset,
        CancellationToken cancellationToken = default)
    {
        var query = _context.UploadedFiles
            .AsNoTracking();

        var totalCount = await query.CountAsync(cancellationToken);

        var items = await query
            .OrderBy(uploadedFile => uploadedFile.Id)
            .Skip(offset)
            .Take(limit)
            .Select(uploadedFile => new ProcessedFileItemDto
            {
                Id = uploadedFile.Id,
                UploadDateTime = uploadedFile.UploadDatetime,
                ProcessedTime = uploadedFile.ProcessedFile == null ? null: uploadedFile.ProcessedFile.ProcessedMilliseconds,
                Status = uploadedFile.Status.ToString().ToLower(),
                Type = uploadedFile.Type.ToString().ToLower(),
                Title = uploadedFile.Filename,
                Txt = uploadedFile.ProcessedFile == null ? null : uploadedFile.ProcessedFile.TxtUrl,
                CorrelationId = uploadedFile.CorrelationId
            })
            .ToListAsync(cancellationToken);

        return new GetFilesPagedResponse { Items = items, TotalCount = totalCount };
    }

    public Task<GetProcessedFileResponse?> GetProcessedFileByCorrelationId(Guid correlationId, CancellationToken cancellationToken = default)
    {
        return _context.ProcessedFiles
            .AsNoTracking()
            .Where(processedFile => processedFile.CorrelationId == correlationId)
            .Select(processedFile => GetProcessedFileResponse.FromProcessedFile(processedFile))
            .FirstOrDefaultAsync(cancellationToken);
    }

    public async Task AddAsync<T>(T item, CancellationToken cancellationToken = default)
    {
        await _context.AddAsync(item!, cancellationToken);
    }

    public void AddRange<T>(IEnumerable<T> items) where T : class, IDomainModel
    {
        _context.Set<T>().AddRange(items);
    }

    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        return _context.SaveChangesAsync(cancellationToken);
    }
}