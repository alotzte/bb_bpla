namespace BPLADetector.Configuration;

public interface IBaseS3Options : IBaseOptions
{ 
    public bool NeedTransformUrl { get; set; }
}