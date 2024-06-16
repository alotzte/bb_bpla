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
    public async Task<ActionResult> UploadFiles(IFormFileCollection files, CancellationToken cancellationToken)
    {
        _logger.LogInformation($"Files: {string.Join(",", files.Select(file => file.FileName))}");

        await _mediator.Send(
            new UploadFileRequest(files.Select(file => file.ToUploadFileItem()).ToList()),
            cancellationToken);

        return Ok();
    }

    [HttpPost("processed-video")]
    public async Task<ActionResult> UploadProcessedVideo(
        [FromHeader] Guid correlationId,
        [FromBody] UploadProcessedVideoRequestDto requestDto,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Uploaded processed file.\nUrl: {url}.\nMarks: [{marks}]", requestDto.Link, string.Join(", ", requestDto.Marks ?? Array.Empty<float>()));
        
        await _mediator.Send(new UploadProcessedVideoRequest(requestDto.Link, requestDto.Marks, correlationId, requestDto.ProcessedMilliseconds), cancellationToken);

        return Ok();
    }
    
    [HttpPost("processed-archive")]
    public async Task<ActionResult> UploadProcessedArchive(
        [FromHeader] Guid correlationId,
        [FromBody] UploadProcessedArchiveRequestDto requestDto,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Uploaded processed file.\nUrl: {url}.", requestDto.Link);
        
        await _mediator.Send(new UploadProcessedArchiveRequest(requestDto.Link, requestDto.Txt, correlationId, requestDto.ProcessedMilliseconds), cancellationToken);

        return Ok();
    }
}