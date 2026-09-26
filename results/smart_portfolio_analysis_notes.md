# Smart Portfolio — Notes pour l'analyse finale

## 1. Objectif
Comparer plusieurs stratégies d'allocation avec un backtest out-of-sample et analyser :
- rendement ;
- volatilité ;
- Sharpe ;
- drawdown ;
- volatility targeting ;
- leverage ;
- turnover ;
- transaction costs ;
- funding costs ;
- robustesse et incertitude statistique.

L'analyse finale doit expliquer les compromis et mécanismes, pas seulement comparer les performances.

## 2. Univers et stratégies
ETF :
SPY, QQQ, EWU, EZU, GLD, VNQ, EEM, IEF, SHY.

Groupes :
- Equities : SPY, QQQ, EWU, EZU, EEM
- Bonds : IEF, SHY
- Alternatives : GLD, VNQ

Stratégies :
Equal Weight, Inverse Vol, Max Geo, Max Sharpe, Carver, Hierarchical Inv Vol, SPY, 60/40, Tech.

SPY, 60/40 et Tech servent de benchmarks simples à comparer aux allocations quantitatives.

## 3. Risk-free rate
Le risk-free est un taux nominal court terme, approximé par les Treasury bills US.

Il sert à calculer le rendement excédentaire :
`excess return = portfolio return - risk-free return`

Pour un portefeuille pleinement investi, le risk-free ne change normalement pas les rendements réalisés ; il change surtout le Sharpe.

Avec volatility targeting :
- somme des poids < 1 : capital résiduel traité comme cash rémunéré au risk-free ;
- somme des poids > 1 : le portefeuille emprunte ; le modèle actuel utilise provisoirement le risk-free comme coût de financement.

Cette dernière hypothèse est simplifiée : en réalité, l'emprunt coûte généralement `risk-free + spread`.

## 4. Sharpe ratio
Utiliser le rendement excédentaire et une moyenne arithmétique :
`Sharpe = mean(Rp - Rf) / volatility(Rp - Rf)`

Le CAGR sert séparément à mesurer la croissance composée.

Point à vérifier dans le code final : `metrics.sharpe_ratio()` doit aligner correctement le risk-free quotidien avec les rendements du portefeuille.

## 5. Résultats RAW actuels

| Strategy | Return | Vol | Sharpe | Drawdown |
|---|---:|---:|---:|---:|
| Equal Weight | 7.35% | 14.60% | 0.462 | -41.58% |
| Inverse Vol | 3.79% | 4.94% | 0.490 | -15.45% |
| Max Geo | 11.51% | 16.22% | 0.665 | -39.30% |
| Max Sharpe | 6.86% | 9.06% | 0.621 | -24.66% |
| Carver | 3.19% | 3.38% | 0.526 | -10.05% |
| Hierarchical Inv Vol | 3.35% | 3.69% | 0.526 | -10.23% |
| SPY | 11.40% | 19.74% | 0.574 | -51.48% |
| 60/40 | 8.30% | 11.11% | 0.645 | -31.45% |
| Tech | 16.43% | 22.41% | 0.728 | -49.37% |

### Points importants
- Tech/QQQ a le rendement le plus élevé dans les résultats actuels, mais aussi la volatilité la plus élevée et un drawdown important.
- SPY est un benchmark equity simple : rendement élevé mais risque et drawdown élevés.
- Carver et Hierarchical Inv Vol ont une volatilité et des drawdowns beaucoup plus faibles, avec un rendement absolu plus faible.
- Max Geo combine rendement élevé et volatilité élevée.
- Max Sharpe utilise directement le risk-free dans son optimisation, donc l'ajout du risk-free peut modifier ses poids, contrairement aux stratégies qui ne l'utilisent pas directement.

## 6. Volatility targeting
Paramètres actuels :
- target = 10%
- max leverage = 2x

Formule :
`leverage = target volatility / estimated portfolio volatility`

puis `leverage <= 2`.

Volatility targeting peut donc :
- réduire l'exposition (<1x) ;
- laisser l'exposition proche de 1x ;
- augmenter l'exposition (>1x).

La volatilité réalisée n'est pas nécessairement exactement 10%, notamment à cause de l'estimation, du rebalance mensuel et du leverage cap.

## 7. Résultats VOL TARGETED actuels

| Strategy | Return | Vol | Sharpe | Drawdown |
|---|---:|---:|---:|---:|
| Equal Weight | 5.30% | 10.86% | 0.399 | -30.48% |
| Inverse Vol | 5.00% | 9.00% | 0.429 | -29.37% |
| Max Geo | 8.18% | 10.57% | 0.663 | -24.00% |
| Max Sharpe | 7.87% | 8.39% | 0.776 | -20.82% |
| Carver | 4.84% | 6.73% | 0.524 | -20.30% |
| Hierarchical Inv Vol | 5.07% | 7.30% | 0.519 | -20.64% |
| SPY | 6.64% | 11.06% | 0.508 | -30.88% |
| 60/40 | 7.60% | 11.11% | 0.587 | -30.92% |
| Tech | 8.48% | 10.64% | 0.685 | -26.98% |

## 8. Leverage : résultats clés

| Strategy | Avg | Max | Min | Time at 2x |
|---|---:|---:|---:|---:|
| Equal Weight | 0.798x | 1.274x | 0.394x | 0% |
| Inverse Vol | 1.843x | 2x | 1.430x | 60.9% |
| Max Geo | 0.629x | 0.935x | 0.358x | 0% |
| Max Sharpe | 1.596x | 2x | 0.505x | 60.0% |
| Carver | 1.992x | 2x | 1.850x | 91.1% |
| Hierarchical Inv Vol | 1.982x | 2x | 1.758x | 88.4% |
| SPY | 0.584x | 0.879x | 0.326x | 0% |
| 60/40 | 1.022x | 1.541x | 0.585x | 0% |
| Tech | 0.493x | 0.746x | 0.330x | 0% |

### Interprétation
**Carver :** leverage moyen ≈1.99x et 91.1% des rebalances à 2x. Le cap de 2x est donc très souvent contraignant.

**Hierarchical Inv Vol :** même mécanisme, avec 88.4% du temps au cap.

**Tech :** leverage moyen ≈0.49x et jamais à 2x. Sa volatilité de base est élevée ; le volatility targeting réduit fortement l'exposition.

Point général :
`sum(weights)` après scaling est proche du leverage. Un leverage >1 signifie exposition supérieure au capital ; <1 signifie qu'une partie du capital reste en cash.

## 9. Pourquoi conserver le leverage history
Il n'est pas nécessaire pour calculer le turnover.

Il sert à :
1. savoir combien de levier la stratégie utilise réellement ;
2. détecter si le leverage cap contraint la stratégie ;
3. expliquer les résultats du volatility targeting ;
4. analyser les funding costs ;
5. comparer des stratégies ayant des performances similaires mais des niveaux de levier différents.

## 10. Spread / funding
Le spread est la prime au-dessus du risk-free payée sur l'emprunt.

Exemple :
- risk-free = 4%
- spread = 2%
- borrowing rate = 6%

Le spread devient important pour les stratégies utilisant beaucoup de leverage.

Version plus réaliste :
`borrowing rate = risk-free + spread`

À faire après turnover et transaction costs.

## 11. Turnover
Le turnover mesure la quantité de portefeuille achetée/vendue lors d'un rebalance :

`turnover_t = 0.5 * sum(abs(target_weights - current_weights))`

Il faut comparer :
- `current_weights` : poids après la dérive pendant la période ;
- `target_weights` : nouveaux poids décidés au rebalance.

Dans le code, `simulate_holding_period()` calcule déjà `end_weights`. Ces `end_weights` sont donc importants pour le turnover.

Leverage history n'est pas nécessaire au turnover.

## 12. Transaction costs
Une fois le turnover calculé :
`transaction_cost = turnover * cost_per_unit`

Exemple :
20% de turnover avec 5 bps de coût ≈ 0.01% de coût.

À analyser :
- turnover par stratégie ;
- performance nette après coûts ;
- sensibilité à différents coûts ;
- dépendance à un rebalancement fréquent.

## 13. Contrôles déjà effectués
- Pour Equal Weight raw, ajouter le risk-free n'a pas changé les rendements réalisés : différence numérique ≈4e-17.
- Le leverage cap fonctionne : Carver max = 2.0.
- Pour Carver, la somme des poids targetés est cohérente avec le leverage : moyenne ≈1.992, max =2.

## 14. Robustesse à faire
Tester :
- estimation window : 1, 3, 5 ans ;
- rebalance : 5, 21, 63 jours ;
- volatility target : 5%, 10%, 15% ;
- leverage cap : 1x, 1.5x, 2x.

Le leverage cap est particulièrement important pour Carver et Hierarchical Inv Vol.

## 15. Sous-périodes à analyser
- 2008–2012 ;
- 2013–2019 ;
- 2020–2021 ;
- 2022 ;
- 2023–2026.

Objectif : vérifier si les résultats globaux sont stables selon les régimes de marché.

## 16. Statistical significance
Les différences de Sharpe doivent être accompagnées d'une mesure d'incertitude.

Prévoir :
- block bootstrap ;
- distribution bootstrap des Sharpe ;
- intervalles de confiance ;
- éventuellement bootstrap des différences de Sharpe.

Le block bootstrap est préférable à un bootstrap i.i.d. simple pour préserver une partie de la dépendance temporelle des rendements.

## 17. Graphiques finaux
À produire :
1. wealth curve ;
2. drawdown/underwater ;
3. weight history pour quelques stratégies ;
4. leverage history pour les portfolios targetés ;
5. éventuellement tableau final net des coûts.

Pour le leverage, une ligne horizontale à 2x sera particulièrement utile pour Carver.

## 18. Structure de l'analyse finale
### A. Methodology
Données, univers, fenêtre d'estimation, rebalance, risk-free, métriques.

### B. Raw portfolios
Performance, risque, drawdowns, benchmarks.

### C. Volatility targeting
Impact sur rendement, risque et drawdown.

### D. Leverage
Leverage moyen, maximum, temps au cap ; focus Carver/Hierarchical Inv Vol et Tech.

### E. Trading frictions
Turnover, transaction costs, funding spread.

### F. Robustness
Windows, fréquence, target, leverage cap, sous-périodes.

### G. Statistical significance
Bootstrap et intervalles de confiance.

### H. Limitations
Univers limité, estimation error, coûts simplifiés, funding simplifié, absence de market impact détaillé, historique non prédictif du futur.

### I. Conclusion
Décrire les compromis et conditions observés plutôt que produire uniquement un classement.

## 19. Checklist

- [x] Risk-free intégré
- [x] Sharpe avec excess returns
- [x] Max Sharpe utilisant le risk-free
- [x] Cash/funding dans le modèle
- [x] Leverage history
- [x] Leverage cap vérifié
- [x] Sanity checks
- [ ] Turnover
- [ ] Transaction costs
- [ ] Funding spread
- [ ] Performance nette
- [ ] Block bootstrap
- [ ] Confidence intervals
- [ ] Parameter sensitivity
- [ ] Subperiod analysis
- [ ] Drawdown plot
- [ ] Weight plots
- [ ] Leverage plot
- [ ] Final table
- [ ] README
- [ ] Tests documentés
- [ ] Limitations documentées

## 20. Messages clés possibles
- Un rendement élevé doit être interprété avec la volatilité et le drawdown.
- Tech/QQQ a actuellement le rendement le plus élevé, mais aussi une volatilité et un drawdown élevés.
- Carver et Hierarchical Inv Vol ont une faible volatilité mais utilisent presque constamment le leverage maximum sous un target de 10%.
- Carver est particulièrement dépendant du cap de 2x.
- Tech est au contraire fortement désendetté par le volatility targeting.
- Le volatility targeting dépend fortement de l'estimation de volatility et du leverage cap.
- Turnover, transaction costs et funding costs peuvent modifier les résultats.
- La robustesse et l'incertitude statistique doivent être analysées avant de tirer des conclusions générales.
