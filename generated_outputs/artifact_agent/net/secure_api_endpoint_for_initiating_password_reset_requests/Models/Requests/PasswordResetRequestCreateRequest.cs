namespace SecureApiEndpoint.Models.Requests;

public class PasswordResetRequestCreateRequest
{
    public string Email { get; set; } = string.Empty;
    public string? ResetToken { get; set; }
}