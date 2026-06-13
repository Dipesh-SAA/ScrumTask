using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace CalculatorApi.Controllers;

[ApiController]
[Route("[controller]")]
public class CalculationsController : ControllerBase
{
    [HttpPost]
    public IActionResult CreateCalculation([FromBody] CalculationCreateRequest request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(new ErrorResponse
                {
                    Error = "BadRequest",
                    Message = "Invalid request data",
                    StatusCode = 400
                });
            }

            double result = request.Operation switch
            {
                "add" => request.Operand1 + request.Operand2,
                "subtract" => request.Operand1 - request.Operand2,
                "multiply" => request.Operand1 * request.Operand2,
                "divide" => request.Operand1 / request.Operand2,
                _ => throw new InvalidOperationException("Invalid operation")
            };

            var response = new CalculationResponse
            {
                Id = Guid.NewGuid().ToString(),
                Operand1 = request.Operand1,
                Operand2 = request.Operand2,
                Operation = request.Operation,
                Result = result,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            return CreatedAtAction(nameof(CreateCalculation), response);
        }
        catch (DivideByZeroException)
        {
            return BadRequest(new ErrorResponse
            {
                Error = "BadRequest",
                Message = "Cannot divide by zero",
                StatusCode = 400
            });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new ErrorResponse
            {
                Error = "InternalServerError",
                Message = ex.Message,
                StatusCode = 500
            });
        }
    }
}