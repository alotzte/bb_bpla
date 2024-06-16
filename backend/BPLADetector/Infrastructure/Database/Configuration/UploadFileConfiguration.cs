using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BPLADetector.Infrastructure.Database.Configuration;

public class UploadFileConfiguration : IEntityTypeConfiguration<UploadedFile>
{
    public void Configure(EntityTypeBuilder<UploadedFile> builder)
    {
        builder.ToTable("upload_file", "domain");

        builder.HasKey(uploadedFile => uploadedFile.Id);

        builder.Property(uploadedFile => uploadedFile.Id)
            .HasColumnName("id");

        builder.Property(uploadedFile => uploadedFile.UploadDatetime)
            .HasColumnName("upload_datetime")
            .IsRequired();

        builder.Property(uploadedFile => uploadedFile.Filename)
            .IsRequired()
            .HasMaxLength(1000)
            .HasColumnName("filename");

        builder.Property(feature => feature.Uri)
            .IsRequired()
            .HasColumnName("uri");

        builder.Property(uploadFile => uploadFile.Type)
            .IsRequired()
            .HasColumnName("type")
            .HasConversion(value => value.ToString(),
                value => (FileType)Enum.Parse(typeof(FileType), value));

        builder.Property(uploadFile => uploadFile.Status)
            .IsRequired()
            .HasColumnName("status")
            .HasConversion(value => value.ToString(),
                value => (UploadStatus)Enum.Parse(typeof(UploadStatus), value));

        builder.Property(uploadFile => uploadFile.CorrelationId)
            .HasColumnName("correlation_id");
    }
}