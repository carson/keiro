#ifndef _PARTICLE_HPP
#define _PARTICLE_HPP

#include <vector>
#include <deque>
#include <cstdio>
#include "vector2d.hpp"

class ParticleState {
public:
	Vec2d position;
	float angle;
};

class World;
class Particle : public ParticleState {
	friend class World;
	World *world;
	std::deque<ParticleState> path;
public:
	Particle(float x=0, float y=0, float dir=1);
	virtual ~Particle();
	float radius;
	Vec2d velocity;  // Current velocity of the particle, setting it directly has no effect. Gets updated by the internals of the update()-mechanism using waypoint logic
	// TODO make hidden/protected and use getter function for getting it to avoid people setting it expecting a change in velocity. Or rename it to current_velocity
	
	float speed; // max speed of the particle TODO: rename to max speed
	float turningspeed; // max turning speed of the particle TODO: rename to max speed
	int collisions; // counter for the number of collisions this particle has been in
	Vec2d previous_position;
	

	void waypoint_clear();
	void waypoint_push(const Vec2d &v);
	void waypoint_push(const Vec2d &v, float angle);
	void waypoint_pop();
	void waypoint_pop_first();
	int waypoint_len() const;
	const ParticleState &waypoint(int i=0) const;
	virtual void update(float dt) = 0;
	void set_state(const Vec2d &v, float angle);
};

class Obstacle {
	friend class World;
	World *world;
public:
	Obstacle(const Vec2d &p1, const Vec2d &p2);
	~Obstacle();
	Vec2d p1, p2;
};

class World{
public:
	World(){}
	~World();
	void bind(Particle *p);
	void unbind(Particle *p);
	void bind(Obstacle *l);
	void unbind(Obstacle *l);
	void update(float dt);
	int num_particles();
	std::vector<Particle*> particles_in_range(const Particle *from, float range) const;
	std::vector<Particle*> particles_in_view_range(const Particle *from, float range) const;
	std::vector<Obstacle*> get_obstacles() const;
private:
	std::vector<Particle*> particles;
	std::vector<Obstacle*> obstacles;
};

#endif