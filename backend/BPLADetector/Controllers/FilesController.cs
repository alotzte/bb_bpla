using BPLADetector.Application.Handlers.File.GetProcessedFile;
using BPLADetector.Application.Handlers.Results.GetProcessedFiles;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace BPLADetector.Controllers;

[ApiController]
[Route("/api/v1/files")]
public class FilesController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ILogger<FilesController> _logger;

    public FilesController(ILogger<FilesController> logger, IMediator mediator)
    {
        _logger = logger;
        _mediator = mediator;
    }

    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(GetFilesPagedResponse), StatusCodes.Status200OK)]
    public async Task<ActionResult<GetProcessedFileResponse>> GetProcessedFile(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        _logger.LogDebug("Получен запрос на получение обработанного файла с id {id}", id);

        var result = await _mediator.Send(new GetProcessedFileRequest(id), cancellationToken);

        return Ok(result);
    }
}