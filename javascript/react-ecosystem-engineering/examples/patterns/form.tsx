import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
const draftSchema = z.object({ title: z.string().trim().min(1).max(120), quantity: z.string().regex(/^\d{1,6}$/) }).strict();
type Draft = { title: string; quantity: string };
type Input = { title: string; quantity: number };
/** No resolver-major assumption: parse explicitly at the submit boundary. */
export function OrderForm({ save }: { save: (input: Input) => Promise<void> }) {
  const { register, handleSubmit, setError, formState: { errors, isSubmitting } } = useForm<Draft>({ defaultValues: { title: '', quantity: '' } });
  const [status, setStatus] = useState('');
  const submit = handleSubmit(async draft => {
    setStatus('');
    const parsed = draftSchema.safeParse(draft);
    if (!parsed.success) {
      for (const issue of parsed.error.issues) {
        const field = issue.path[0];
        if (field === 'title' || field === 'quantity') setError(field, { message: issue.message });
      }
      return;
    }
    try { await save({ title: parsed.data.title, quantity: Number(parsed.data.quantity) }); setStatus('Saved.'); }
    catch { setStatus('Save failed. Your draft is preserved.'); }
  });
  return <form onSubmit={submit} noValidate>
    <label htmlFor="order-title">Title</label>
    <input id="order-title" {...register('title')} aria-invalid={!!errors.title} aria-describedby="order-title-error" />
    <span id="order-title-error">{errors.title?.message}</span>
    <label htmlFor="order-quantity">Quantity</label>
    <input id="order-quantity" inputMode="numeric" {...register('quantity')} aria-invalid={!!errors.quantity} aria-describedby="order-quantity-error" />
    <span id="order-quantity-error">{errors.quantity?.message}</span>
    <button disabled={isSubmitting}>Save</button><p role="status">{status}</p>
  </form>;
}
