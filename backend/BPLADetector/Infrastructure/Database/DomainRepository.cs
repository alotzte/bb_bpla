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

    public async Task<GetProcessedFilesResponse> GetProcessedFiles(
        int limit,
        int offset,
        CancellationToken cancellationToken = default)
    {
        var query = _context.ProcessedFiles
            .AsNoTracking();

        var totalCount = await query.CountAsync(cancellationToken);

        var items = await query
            .OrderBy(procesedFile => procesedFile.Id)
            .Skip(offset)
            .Take(limit)
            .Select(processedFile => new ProcessedFileItemDto
            {
                Id = processedFile.Id,
                UploadDateTime = processedFile.UploadedFile != null ? processedFile.UploadedFile.UploadDatetime : null,
                ProcessedTime = processedFile.ProcessedMilliseconds,
                Status = processedFile.UploadedFile != null
                    ? processedFile.UploadedFile.Status.ToString().ToLower()
                    : null,
                Type = processedFile.Type.ToString().ToLower(),
                Title = processedFile.Filename,
                Txt = processedFile.TxtUrl,
            })
            .ToListAsync(cancellationToken);

        return new GetProcessedFilesResponse { Items = items, TotalCount = totalCount };
    }

    public Task<GetProcessedFileResponse?> GetProcessedFileById(long id, CancellationToken cancellationToken = default)
    {
        return _context.ProcessedFiles
            .AsNoTracking()
            .Where(file => file.Id == id)
            .Select(file => GetProcessedFileResponse.FromProcessedFile(file))
            .FirstOrDefaultAsync(cancellationToken);
    }

    public async Task AddAsync<T>(T item, CancellationToken cancellationToken = default)
    {
        await _context.AddAsync(item!, cancellationToken);
    }

    public void AddRange<T>(IEnumerable<T> items) where T : class
    {
        _context.Set<T>().AddRange(items);
    }

    public void Update<T>(T item) where T : class
    {
        _context.Set<T>().Update(item);
    }

    public void UpdateRange<T>(IEnumerable<T> items) where T : class
    {
        _context.Set<T>().UpdateRange(items);
    }

    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        return _context.SaveChangesAsync(cancellationToken);
    }
}