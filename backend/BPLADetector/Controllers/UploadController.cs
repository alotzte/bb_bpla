using BPLADetector.Application.DTO;
using BPLADetector.Application.Handlers.Upload.UploadFile;
using BPLADetector.Application.Handlers.Upload.UploadProcessedArchive;
using BPLADetector.Application.Handlers.Upload.UploadProcessedVideo;
using BPLADetector.Infrastructure.Extensions;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace BPLADetector.Controllers;

[ApiController]
[Route("api/v1/upload")]
public class UploadController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ILogger<UploadController> _logger;

    public UploadController(ILogger<UploadController> logger, IMediator mediator)
    {
        _logger = logger;
        _mediator = mediator;
    }

    [HttpPost]
    [RequestSizeLimit(1_100_000_000)]
    public async Task<ActionResult> UploadFiles(IFormFileCollection files, CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            $"Получен запрос на загрузку файлов: {string.Join(",", files.Select(file => file.FileName))}");

        await _mediator.Send(
            new UploadFileRequest(
                files.Select(file => file.ToUploadFileItem()).ToList()),
            cancellationToken);

        _logger.LogInformation($"Файлы {string.Join(",", files.Select(file => file.FileName))} успешно загружены.");

        return Ok();
    }

    [HttpPost("single")]
    [RequestSizeLimit(1_100_000_000)]
    public async Task<ActionResult> UploadFile(IFormFile file, CancellationToken cancellationToken)
    {
        _logger.LogInformation($"Получен запрос на загрузку файла: {file.FileName}");

        await _mediator.Send(
            new UploadFileRequest(
                new List<UploadFileItem> { file.ToUploadFileItem() }),
            cancellationToken);

        _logger.LogInformation($"Файл {file.FileName} успешно загружен");

        return Ok();
    }

    [HttpPost("processed-video")]
    public async Task<ActionResult> UploadProcessedVideo(
        [FromHeader] Guid correlationId,
        [FromBody] UploadProcessedVideoRequestDto requestDto,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Получен запрос на загрузу обработанного видео {correlationId}.\nUrl: {url}.\nMarks: [{marks}]",
            correlationId, 
            requestDto.Link,
            string.Join(", ", requestDto.Marks ?? Array.Empty<float>()));

        await _mediator.Send(
            new UploadProcessedVideoRequest(requestDto.Link, requestDto.Marks, correlationId,
                requestDto.ProcessedMilliseconds), cancellationToken);

        _logger.LogInformation($"Обработанное видео {correlationId} загружено успешно");
        
        return Ok();
    }

    [HttpPost("processed-archive")]
    public async Task<ActionResult> UploadProcessedArchive(
        [FromHeader] Guid correlationId,
        [FromBody] UploadProcessedArchiveRequestDto requestDto,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Получен запрос на загрузку обработанного архива {correlationId}.\nUrl: {url}.", correlationId, requestDto.Link);

        await _mediator.Send(
            new UploadProcessedArchiveRequest(requestDto.Link, requestDto.Txt, correlationId,
                requestDto.ProcessedMilliseconds), cancellationToken);
        
        _logger.LogInformation($"Обработанный архив {correlationId} успешно загружен.");
        
        return Ok();
    }
}