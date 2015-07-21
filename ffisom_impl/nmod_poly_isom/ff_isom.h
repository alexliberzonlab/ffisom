/*
 * ffIsomorphism.h
 *
 *  Created on: Dec 3, 2013
 *      Author: javad
 */

#ifndef FFISOMORPHISM_H_
#define FFISOMORPHISM_H_

#include <flint/fq_nmod.h>
#include <flint/fq_nmod_poly.h>

class FFIsomorphism {

	fq_nmod_ctx_t ctx_1;
	fq_nmod_ctx_t ctx_2;
	nmod_poly_t x_image;
	nmod_mat_t isom_mat;

	fq_nmod_poly_t delta_init;
	nmod_poly_t delta_init_trivial;
	fq_nmod_t xi_init;
	nmod_poly_t xi_init_trivial;
	
	const static int TRACE_THRESHOLD = 1000;

	void compute_semi_trace_small_ext(fq_nmod_poly_t delta, fq_nmod_t xi, slong n, const fq_nmod_ctx_t ctx, const fq_nmod_poly_t modulus);
	void compute_semi_trace_trivial_ext(nmod_poly_t delta, nmod_poly_t xi, slong n, const nmod_poly_t modulus, const mp_limb_t z);
	void compute_semi_trace_trivial_ext(nmod_poly_t theta, const nmod_poly_t a, const nmod_poly_t modulus, mp_limb_t z);
	void compute_semi_trace_small_ext(fq_nmod_poly_t theta, const fq_nmod_poly_t a, const fq_nmod_ctx_t ctx, const fq_nmod_poly_t modulus);
	void compute_semi_trace_large_ext(fq_nmod_poly_t theta, const fq_nmod_t alpha, const fq_nmod_ctx_t ctx, const fq_nmod_poly_t modulus);
	void compute_semi_trace(fq_nmod_poly_t theta, const fq_nmod_ctx_t ctx, const fq_nmod_poly_t modulus);
	void compute_xi(fq_nmod_t xi, const fq_nmod_t old_xi, const fq_nmod_ctx_t ctx);
	void compute_delta(fq_nmod_poly_t delta, const fq_nmod_t xi, slong z_degree, const fq_nmod_ctx_t ctx, const fq_nmod_poly_t modulus);
	void compute_xi_init(const fq_nmod_ctx_t ctx, slong s);
	void iterated_frobenius(fq_nmod_t *result, const fq_nmod_t alpha, const fq_nmod_ctx_t ctx, slong s);
	void compute_extension_isomorphism(fq_nmod_poly_t f, fq_nmod_poly_t f_image);
	void compute_middle_isomorphism(fq_nmod_t c, const fq_nmod_poly_t theta_a, const fq_nmod_poly_t theta_b, const fq_nmod_poly_t modulus,
			const fq_nmod_ctx_t cyclotomic_ctx);
	void build_cyclotomic_extension(fq_nmod_poly_t modulus, fq_nmod_ctx_t cyclotomic_ctx);
	void convert(fq_nmod_t result, const fq_nmod_poly_t value, const fq_nmod_ctx_t ctx);
	void convert(fq_nmod_poly_t result, const fq_nmod_t value, const fq_nmod_ctx_t ctx);
	mp_limb_t compute_cyclotomic_root(const slong r, const mp_limb_t p);
	void compute_semi_trace(nmod_poly_t theta, const nmod_poly_t modulus, const mp_limb_t z);
	void compute_extension_isomorphism(nmod_poly_t f, nmod_poly_t f_image);

public:

	FFIsomorphism(const nmod_poly_t f1, const nmod_poly_t f2);
	void compute_generators(nmod_poly_t f1, nmod_poly_t f2);
	void build_isomorphism(const nmod_poly_t f1, const nmod_poly_t f2);
	void compute_isom_matrix();
	void get_x_image(nmod_poly_t x_image);
	void compute_image_using_modcomp(nmod_poly_t image, const nmod_poly_t f);
	void compute_image_using_matrix(nmod_poly_t image, const nmod_poly_t f);
	~FFIsomorphism();
};

#endif /* FFISOMORPHISM_H_ */