package com.example.calculatorapi.controller;

import com.example.calculatorapi.model.CalculationCreateRequest;
import com.example.calculatorapi.model.CalculationResponse;
import com.example.calculatorapi.model.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.UUID;

@RestController
@RequestMapping("/calculations")
public class CalculationController {
    @PostMapping
    public ResponseEntity<?> createCalculation(@RequestBody CalculationCreateRequest request) {
        try {
            double result;
            switch (request.getOperation()) {
                case "add" -> result = request.getOperand1() + request.getOperand2();
                case "subtract" -> result = request.getOperand1() - request.getOperand2();
                case "multiply" -> result = request.getOperand1() * request.getOperand2();
                case "divide" -> {
                    if (request.getOperand2() == 0) {
                        return ResponseEntity.badRequest().body(
                            new ErrorResponse("Division by zero", "Operand2 cannot be zero for division", 400)
                        );
                    }
                    result = request.getOperand1() / request.getOperand2();
                }
                default -> {
                    return ResponseEntity.badRequest().body(
                        new ErrorResponse("Invalid operation", "Operation must be one of: add, subtract, multiply, divide", 400)
                    );
                }
            }

            CalculationResponse response = new CalculationResponse(
                UUID.randomUUID().toString(),
                request.getOperand1(),
                request.getOperand2(),
                request.getOperation(),
                result,
                Instant.now()
            );
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(
                new ErrorResponse("Internal server error", e.getMessage(), 500)
            );
        }
    }
}