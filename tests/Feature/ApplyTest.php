<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Symfony\Component\HttpFoundation\Response;
use Tests\TestCase;

class ApplyTest extends TestCase
{
    use RefreshDatabase;

    protected $ENDPOINT = '/api/loan';

    protected function setUp(): void
    {
        parent::setUp();
        $this->withHeaders([
            'Accept' => 'application/json',
        ]);
    }

    public function test_missing_credential()
    {
        $response = $this->post($this->ENDPOINT);
        $response->assertStatus(Response::HTTP_UNAUTHORIZED);
    }

    public function test_missing_param()
    {
        $user = User::factory()->create();
        $response = $this->actingAs($user)->post($this->ENDPOINT);
        $response->assertStatus(Response::HTTP_UNPROCESSABLE_ENTITY);
    }

    public function test_malformed_param()
    {
        $user = User::factory()->create();
        $response = $this->actingAs($user)->post($this->ENDPOINT, [
            'amount' => 'NaN',
        ]);
        $response->assertStatus(Response::HTTP_UNPROCESSABLE_ENTITY);
    }

    public function test_success()
    {
        $amount = 100;
        $due = date('Y-m-d', strtotime('+1 year'));
        $user = User::factory()->create();
        $response = $this->actingAs($user)->post($this->ENDPOINT, [
            'amount' => $amount,
            'due' => $due,
        ]);
        $response->assertStatus(Response::HTTP_CREATED);
        $this->assertDatabaseHas('loans', [
            'user_id' => 1,
            'amount' => $amount,
            'due' => $due,
        ]);
    }
}
