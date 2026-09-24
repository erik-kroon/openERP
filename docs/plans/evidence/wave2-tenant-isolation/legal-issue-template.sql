DO $exercise$
DECLARE s jsonb:='{"entityId":"__ENTITY__","bookId":"__BOOK__"}';
 one text:='__TOKEN_ONE__';
 two text:='__TOKEN_TWO__';
 three text:='__TOKEN_THREE__';
 seller jsonb; buyer jsonb; rule jsonb; ref_seller jsonb; ref_buyer jsonb; ref_rule jsonb;
 party jsonb; draft jsonb; candidate jsonb; review jsonb; policy jsonb; accounting jsonb;
 issue_review jsonb; approval jsonb; issued jsonb; input jsonb; cnt integer;
BEGIN
 INSERT INTO openerp.actors VALUES('__ACTOR_TWO__','Independent policy reviewer'),('__ACTOR_THREE__','Policy activator');
 INSERT INTO openerp.memberships VALUES('__BOOK__','__ACTOR_TWO__','operator'),('__BOOK__','__ACTOR_THREE__','operator');
 INSERT INTO openerp.credentials(token_hash,actor_id,expires_at)
 VALUES(encode(sha256(convert_to(two,'UTF8')),'hex'),'__ACTOR_TWO__','2026-12-31'),
       (encode(sha256(convert_to(three,'UTF8')),'hex'),'__ACTOR_THREE__','2026-12-31');
 INSERT INTO openerp.accounts(book_id,id,code,name) VALUES
  ('__BOOK__','account_ar','1510','Customer receivables'),
  ('__BOOK__','account_revenue','3010','Domestic sales'),
  ('__BOOK__','account_vat','2611','Output VAT 25%');
 seller:=openerp.create_evidence(one,s,'ar_seller_evidence_001',jsonb_build_object('title','Seller legal assertion','mediaType','text/plain','content','synthetic Swedish seller 556123-4567','origin','manual temporary review fixture'));
 buyer:=openerp.create_evidence(one,s,'ar_buyer_evidence_001',jsonb_build_object('title','Customer legal assertion','mediaType','text/plain','content','synthetic Swedish buyer 556987-6543','origin','manual temporary review fixture'));
 rule:=openerp.create_evidence(one,s,'ar_rule_evidence_001',jsonb_build_object('title','Policy evidence','mediaType','text/plain','content','Synthetic review fixture for Swedish domestic standard 25%; not independent legal authority','origin','manual temporary review fixture'));
 ref_seller:=jsonb_build_object('evidenceId',seller->>'id','sha256',seller->>'sha256');
 ref_buyer:=jsonb_build_object('evidenceId',buyer->>'id','sha256',buyer->>'sha256');
 ref_rule:=jsonb_build_object('evidenceId',rule->>'id','sha256',rule->>'sha256');
 party:=openerp.commerce_create_counterparty(one,s,'ar_party_create_001',jsonb_build_object(
  'kind','synthetic_counterparty_v1','externalKey','synthetic_buyer_001','role','customer',
  'displayName','Buyer AB','evidenceId',buyer->>'id','reason','Explicit synthetic legal buyer evidence'));
 draft:=openerp.create_invoice_draft(one,s,'ar_draft_create_001',jsonb_build_object('draftKey','ar_native_001',
  'content',jsonb_build_object('title','Accounting services September','counterpartyId',party->>'id',
  'counterpartyRevision',party->>'revision',
  'seller',jsonb_build_object('legalName','Seller AB','registrationId','556123-4567','taxId','SE556123456701',
   'address','Seller Street 1, 11111 Stockholm','countryCode','SE','evidenceId',seller->>'id'),
  'customer',jsonb_build_object('legalName','Buyer AB','registrationId','556987-6543','taxId',NULL,
   'address','Buyer Street 2, 22222 Stockholm','countryCode','SE','evidenceId',buyer->>'id'),
  'currency','SEK','currencyScale',2,'plannedIssueDate','__ISSUE_DATE__','supplyDate','__ISSUE_DATE__',
  'dueDate','__DUE_DATE__','paymentTerms','30 days','sourceTotalMinor','12500',
  'lines',jsonb_build_array(jsonb_build_object('id','line_one','description','Domestic consulting service',
   'quantity','1','unitPriceMinor','10000','baseMinor','10000','discountMinor','0','chargeMinor','0',
   'taxMinor','2500','taxDescription','se-domestic-standard-25-v1','taxEvidenceId',rule->>'id',
   'sourceGrossMinor','12500')))));
 candidate:=openerp.save_invoice_policy_candidate(one,s,'ar_candidate_save_001',jsonb_build_object(
  'profileKey','seller_policy_se25_v1',
  'sellerIdentity',jsonb_build_object('legalName','Seller AB','registrationNumber','556123-4567',
    'vatRegistrationNumber','SE556123456701','postalAddress','Seller Street 1, 11111 Stockholm','countryCode','SE'),
  'sellerEvidence',ref_seller,'legalNumbering','sequential-per-series-v1','numberingEvidence',ref_rule,
  'vatTreatment','se-domestic-standard-25-v1','vatEvidence',ref_rule,
  'roundingMethod','line-tax-half-up-minor-v1','roundingEvidence',ref_rule,
  'creditNotePolicy','unsupported','correctionPolicy','unsupported','correctionEvidence',ref_rule,
  'effectiveFrom','__ISSUE_DATE__','reason','Review narrow domestic accrual policy','acknowledgeUnactivated',true));
 review:=openerp.review_invoice_policy_candidate(two,s,candidate->>'id','ar_candidate_review_001',jsonb_build_object(
  'candidateDigest',candidate->>'digest','reviewEvidence',ref_rule,'findings','Independently reviewed synthetic scenario',
  'acknowledgeNoLegalActivation',true));
 policy:=openerp.activate_ar_legal_policy(three,s,'ar_policy_activate_001',jsonb_build_object(
  'candidateId',candidate->>'id','candidateDigest',candidate->>'digest',
  'reviewId',review->>'id','reviewDigest',review->>'digest','series','AR',
  'ruleVersion','se-domestic-standard-25-2023-200-v1','sourceEvidence',ref_rule,
  'activationEvidence',ref_rule,'reason','Activate review fixture','acceptReviewedPolicy',true,'acknowledgeIssueBlocked',true));
 accounting:=openerp.activate_ar_legal_accounting_profile(one,s,'ar_account_profile_001',jsonb_build_object(
  'policyId',policy->>'id','policyDigest',policy->>'digest','profile','se-domestic-b2b-sek-25-accrual-v1',
  'accountingMethod','accrual','ruleVersion','se-domestic-standard-25-2023-200-v1',
  'effectiveFrom','__ISSUE_DATE__','controlAccountId','account_ar','revenueAccountId','account_revenue',
  'outputVatAccountId','account_vat','accountRoleEvidence',ref_rule,'reason','Bind exact reviewed account roles',
  'acceptLegalAccounting',true));
 input:=jsonb_build_object('profile','se-domestic-b2b-sek-25-accrual-v1','draftId',draft->>'id',
  'expectedRevision',draft->>'revision','expectedDigest',draft->>'digest','policyId',policy->>'id',
  'policyDigest',policy->>'digest','accountingProfileId',accounting->>'id',
  'accountingProfileDigest',accounting->>'digest','controlAccountId','account_ar',
  'revenueAccountId','account_revenue','outputVatAccountId','account_vat',
  'accountingPeriodId','__PERIOD__','voucherSeries','A',
  'reason','Recognize reviewed domestic supply','acknowledgeLimitedProfile',true);
 issue_review:=openerp.prepare_ar_legal_issue(one,s,'ar_legal_prepare_001',input);
 approval:=openerp.approve_ar_legal_issue(two,s,issue_review->>'id','ar_legal_approve_001',
  jsonb_build_object('version',1,'digest',issue_review->>'digest','acknowledgeLimitedProfile',true));
 issued:=openerp.execute_ar_legal_issue(two,s,issue_review->>'id','ar_legal_execute_001',
  jsonb_build_object('version',1,'digest',issue_review->>'digest',
   'approvalId',approval->>'id','acknowledgeLimitedProfile',true));
 RAISE NOTICE 'AR_ISSUE=% REVIEW=% LEGAL_NUMBER=% VOUCHER=% REGISTER=% TOTALS=%',
  issued->>'id',issue_review->>'id',issued->>'legalDocumentNumber',
  issued->'postingReceipt'->>'voucherId',issued->>'registerInvoiceId',issued->'totals';
END $exercise$;
