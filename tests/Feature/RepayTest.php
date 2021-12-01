<?php

namespace Tests\Feature;

use App\Models\Loan;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Response;
use Tests\TestCase;

class RepayTest extends TestCase
{
    use RefreshDatabase;
    protected $ENDPOINT = '/api/loan/';
    protected $loan;
    protected $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->withHeaders([
            'Accept' => 'application/json',
        ]);
        $this->loan = Loan::factory()->create();
        $this->user = User::find($this->loan->user_id);
    }

    public function test_wrong_user()
    {
        $user = User::factory()->create();
        $resp = $this->actingAs($user)->patch($this->ENDPOINT . $this->loan->id, [
            'amount' => $this->loan->amount - 10,
        ]);
        $resp->assertStatus(Response::HTTP_FORBIDDEN);
        $this->assertTrue($this->loan->isClean());
    }


    public function test_success()
    {
        $amount_orig = $this->loan->amount;
        $amount = $this->loan->amount / 3;
        $resp = $this->actingAs($this->user)->patch($this->ENDPOINT . $this->loan->id, [
            'amount' => $amount,
        ]);
        $resp->assertStatus(Response::HTTP_ACCEPTED);
        $this->loan->refresh();
        $this->assertEqualsWithDelta($amount_orig - $amount, $this->loan->amount, 1e-4);
    }
}
