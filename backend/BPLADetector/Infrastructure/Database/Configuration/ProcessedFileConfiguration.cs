using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BPLADetector.Infrastructure.Database.Configuration;

public class ProcessedFileConfiguration : IEntityTypeConfiguration<ProcessedFile>
{
    public void Configure(EntityTypeBuilder<ProcessedFile> builder)
    {
        builder.ToTable("processed_file", "domain");

        builder.HasKey(processedFile => processedFile.Id);

        builder.Property(processedFile => processedFile.Id)
            .HasColumnName("id");

        builder.Property(processedFile => processedFile.UploadDatetime)
            .HasColumnName("upload_datetime")
            .IsRequired();

        builder.Property(processedFile => processedFile.ProcessedMilliseconds)
            .HasColumnName("processed_milliseconds");

        builder.Property(processedFile => processedFile.Uri)
            .IsRequired()
            .HasColumnName("uri");

        builder.Property(processedFile => processedFile.TxtUrl)
            .HasColumnName("txt_url");

        builder.Property(uploadedFile => uploadedFile.Filename)
            .IsRequired()
            .HasMaxLength(1000)
            .HasColumnName("filename");

        builder.Property(processedFile => processedFile.Type)
            .IsRequired()
            .HasColumnName("type")
            .HasConversion(value => value.ToString(),
                value => (FileType)Enum.Parse(typeof(FileType), value));

        builder.Property(processedFile => processedFile.Marks)
            .HasColumnName("marks");
        
        builder.Property(uploadFile => uploadFile.CorrelationId)
            .HasColumnName("correlation_id");
        
        builder.HasOne(processedFile => processedFile.UploadedFile)
            .WithOne(uploadedFile => uploadedFile.ProcessedFile)
            .HasForeignKey<ProcessedFile>(processedFile => processedFile.CorrelationId)
            .HasPrincipalKey<UploadedFile>(uploadedFile => uploadedFile.CorrelationId)
            .HasConstraintName("upload_file_fk");
    }
}