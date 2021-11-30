<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class LoanFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'user_id' => User::Factory(),
            'amount' => $this->faker->numberBetween(),
            'due' => $this->faker->date('Y-m-d','+20 years'),
        ];
    }
}
