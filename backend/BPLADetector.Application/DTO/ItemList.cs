namespace BPLADetector.Application.DTO;

public class ItemList<T>
{
    public List<T> Items { get; set; }
    public int TotalCount { get; set; }
}