from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Subscription
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    # Check if already active
    today = timezone.now().date()
    active_sub = Subscription.objects.filter(status='active', end_date__gte=today).first()
    if active_sub:
        return redirect('subscription:status')
        
    return render(request, 'subscription/index.html')

@login_required
def payment(request):
    if request.method == 'POST':
        # Simulate payment success
        Subscription.objects.create(
            plan='monthly',
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            amount_paid=3000.00,
            payment_date=timezone.now(),
            transaction_id=f"PAY-{int(timezone.now().timestamp())}"
        )
        messages.success(request, 'Payment Successful! Subscription Active.')
        return redirect('subscription:status')
    return redirect('subscription:index')

@login_required
def status(request):
    today = timezone.now().date()
    # Get the latest subscription
    sub = Subscription.objects.order_by('-created_at').first()
    
    is_active = False
    if sub and sub.status == 'active' and sub.end_date >= today:
        is_active = True
        
    return render(request, 'subscription/status.html', {
        'subscription': sub,
        'is_active': is_active
    })

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def intasend_webhook(request):
    """
    Webhook endpoint to receive payment events from IntaSend.
    Expected at /v1/events or /v1/events/
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            logger.info(f"IntaSend Webhook received: {payload}")
            
            # Example payload: {"invoice_id": "...", "state": "COMPLETED", "value": "100", "api_ref": "..."}
            state = payload.get('state')
            api_ref = payload.get('api_ref')
            invoice_id = payload.get('invoice_id')
            value = payload.get('value', 0)
            
            if state == 'COMPLETED':
                # Create or update subscription
                Subscription.objects.create(
                    plan='monthly',
                    status='active',
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timedelta(days=30),
                    amount_paid=value,
                    payment_date=timezone.now(),
                    transaction_id=invoice_id or f"WEBHOOK-{int(timezone.now().timestamp())}"
                )
                return JsonResponse({'status': 'success', 'message': 'Payment processed successfully'})
            
            return JsonResponse({'status': 'ignored', 'message': f'Payment state {state} ignored'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
