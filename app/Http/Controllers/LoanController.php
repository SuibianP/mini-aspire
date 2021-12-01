<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreLoanRequest;
use App\Http\Requests\UpdateLoanRequest;
use App\Models\Loan;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Auth;

class LoanController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $this->authorize('view_any', Loan::class);
        return new Response(Loan::all());
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreLoanRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreLoanRequest $request)
    {
        $this->authorize('create', Loan::class);
        $loan = new Loan([
            'user_id' => Auth::user()->id,
            'due' => $request->due,
            'amount' => $request->amount,
        ]);
        $loan->save();
        return new Response($loan, Response::HTTP_CREATED);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Loan  $loan
     * @return \Illuminate\Http\Response
     */
    public function show(Loan $loan)
    {
        return new Response($loan, Response::HTTP_FOUND);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateLoanRequest  $request
     * @param  \App\Models\Loan  $loan
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateLoanRequest $request, Loan $loan)
    {
        $this->authorize('update', $loan);
        if ($loan->amount < $request->amount) {
            return new Response("Repay amount exceeding loan amount", Response::HTTP_NOT_ACCEPTABLE);
        }
        $loan->update([
            'amount' => $loan->amount - $request->amount,
        ]);
        $loan->save();
        return new Response($loan, Response::HTTP_ACCEPTED);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Loan  $loan
     * @return \Illuminate\Http\Response
     */
    public function destroy(Loan $loan)
    {
        $this->authorize('delete', Loan::class);
        Loan::destroy($loan->id);
        return new Response('', Response::HTTP_OK);
    }
}
