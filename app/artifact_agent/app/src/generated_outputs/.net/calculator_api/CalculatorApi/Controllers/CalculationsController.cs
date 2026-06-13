using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace CalculatorApi.Controllers;

[ApiController]
[Route("[controller]")]
public class CalculationsController : ControllerBase
{
    private static readonly List<CalculationResponse> _calculations = new();

    [HttpPost]
    public ActionResult<CalculationResponse> CreateCalculation([FromBody] CalculationCreateRequest request)
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

        var result = request.Operation switch
        {
            "add" => request.Operand1 + request.Operand2,
            "subtract" => request.Operand1 - request.Operand2,
            "multiply" => request.Operand1 * request.Operand2,
            "divide" => request.Operand1 / request.Operand2,
            _ => throw new InvalidOperationException("Invalid operation")
        };

        var calculation = new CalculationResponse
        {
            Id = Guid.NewGuid().ToString(),
            Operand1 = request.Operand1,
            Operand2 = request.Operand2,
            Operation = request.Operation,
            Result = result,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        _calculations.Add(calculation);
        return CreatedAtAction(nameof(GetCalculation), new { id = calculation.Id }, calculation);
    }

    [HttpPut("{id}")]
    public ActionResult<CalculationResponse> UpdateCalculation(string id, [FromBody] CalculationUpdateRequest request)
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

        var calculation = _calculations.FirstOrDefault(c => c.Id == id);
        if (calculation == null)
        {
            return NotFound();
        }

        var result = request.Operation switch
        {
            "add" => request.Operand1 + request.Operand2,
            "subtract" => request.Operand1 - request.Operand2,
            "multiply" => request.Operand1 * request.Operand2,
            "divide" => request.Operand1 / request.Operand2,
            _ => throw new InvalidOperationException("Invalid operation")
        };

        calculation.Operand1 = request.Operand1;
        calculation.Operand2 = request.Operand2;
        calculation.Operation = request.Operation;
        calculation.Result = result;
        calculation.UpdatedAt = DateTime.UtcNow;

        return Ok(calculation);
    }

    [HttpDelete("{id}")]
    public IActionResult DeleteCalculation(string id)
    {
        var calculation = _calculations.FirstOrDefault(c => c.Id == id);
        if (calculation == null)
        {
            return NotFound();
        }

        _calculations.Remove(calculation);
        return NoContent();
    }

    [HttpGet]
    public ActionResult<IEnumerable<CalculationResponse>> ListCalculations()
    {
        return Ok(_calculations);
    }

    [HttpGet("{id}")]
    public ActionResult<CalculationResponse> GetCalculation(string id)
    {
        var calculation = _calculations.FirstOrDefault(c => c.Id == id);
        if (calculation == null)
        {
            return NotFound();
        }

        return Ok(calculation);
    }
}