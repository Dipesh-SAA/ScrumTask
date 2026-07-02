using SecureApiEndpoint.Models.Requests;
using SecureApiEndpoint.Models.Responses;
using SecureApiEndpoint.Services.Interfaces;

namespace SecureApiEndpoint.Services.Implementations;

public class PasswordResetRequestService : IPasswordResetRequestService
{
    public async Task<PasswordResetRequestResponse> CreatePasswordResetRequestAsync(PasswordResetRequestCreateRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Email))
        {
            throw new ArgumentException("Email is required.");
        }

        if (!IsValidEmail(request.Email))
        {
            throw new ArgumentException("Invalid email format.");
        }

        // In a real implementation, this would save to a database
        return new PasswordResetRequestResponse
        {
            Id = Guid.NewGuid().ToString(),
            Email = request.Email,
            ResetToken = request.ResetToken ?? GenerateResetToken(),
            IsActive = true,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
    }

    private bool IsValidEmail(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }

    private string GenerateResetToken()
    {
        return Guid.NewGuid().ToString("N").Substring(0, 16);
    }
}