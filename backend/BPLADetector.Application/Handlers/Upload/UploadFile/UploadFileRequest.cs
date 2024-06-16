using BPLADetector.Application.DTO;
using MediatR;

namespace BPLADetector.Application.Handlers.Upload.UploadFile;

public class UploadFileRequest : IRequest
{
    public UploadFileRequest(List<UploadFileItem> items)
    {
        Items = items;
    }

    public List<UploadFileItem> Items { get; set; }
}