# Week 1 Assignment: Real-World Options Advisory Memo

## Advisory Memo

**To:** A beginner investor considering protection for an equity position  
**From:** Pratik Lagad  
**Subject:** How listed options can be used for protection and directional views

## Situation

Assume an investor owns shares of a stock currently trading near 100. The investor
likes the long-term company story but is worried about a short-term fall after an
earnings announcement. Selling the shares would remove the risk, but it would
also remove the upside. Buying a put option is one way to keep the upside while
limiting downside over a defined period.

## What An Option Is

An option is a derivative contract whose value depends on an underlying asset.
The buyer pays a premium and receives a right, not an obligation. The seller
receives the premium and accepts the obligation if the buyer exercises.

The strike price, `K`, is the fixed exercise price. The spot price, `S`, is the
current market price of the underlying. The maturity, `T`, is the time until the
option expires.

## Calls And Puts

A call option gives the holder the right to buy the underlying at the strike.
A put option gives the holder the right to sell the underlying at the strike.

For a call, the expiry payoff is:

```text
max(S - K, 0)
```

For a put, the expiry payoff is:

```text
max(K - S, 0)
```

If the investor owns the stock and fears a fall, the relevant contract is a put.
For example, buying a put with strike 95 creates a floor close to 95 before
considering the premium paid.

## Moneyness

Moneyness describes where the underlying price sits relative to the strike:

| Term | Call Option | Put Option |
| --- | --- | --- |
| In the money | `S > K` | `S < K` |
| At the money | `S approx K` | `S approx K` |
| Out of the money | `S < K` | `S > K` |

Intrinsic value is the payoff if the option were exercised immediately. Time
value is the extra value from uncertainty before expiry.

## European Versus American Exercise

A European option can be exercised only at expiry. An American option can be
exercised any time up to expiry. The American feature is valuable because it
adds flexibility, so an American option should not be worth less than the
corresponding European option.

This distinction matters most for American puts. When a put is deep in the
money and interest rates are positive, early exercise can become optimal because
the holder may prefer receiving the strike cash now instead of waiting.

## What Drives Option Prices

The main drivers are:

- Spot price: puts become more valuable when the underlying falls.
- Strike price: higher put strikes generally make puts more valuable.
- Time to maturity: more time usually increases optionality.
- Volatility: higher volatility increases both call and put values.
- Risk-free rate: affects discounting and early-exercise incentives.

These drivers are later formalized through Greeks such as delta, gamma, vega,
theta, and rho.

## Recommendation

For a shareholder who wants downside protection without selling the stock, a
protective put is suitable. The investor should choose a strike based on the
maximum tolerable loss and choose an expiry that covers the risky event. The
trade-off is cost: the premium reduces total return if the stock does not fall.

For a beginner, the safer use case is buying options for defined-risk exposure
or protection. Selling options should be treated more carefully because the
seller carries obligations and can face large losses.

## Reflection

The key insight from Week 1 is that options are contracts on flexibility. A put
is not just a bet that the stock will fall; it can also work like insurance. The
premium is the price of that insurance, and the option's value changes with
moneyness, time, volatility, rates, and exercise style.

