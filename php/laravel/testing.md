---
tags: [laravel, testing, phpunit, pest, feature-test]
concepts: [tdd, integration-testing, feature-testing]
requires: [php/testing.md, php/laravel/architecture.md]
keywords: [RefreshDatabase, factory, feature-test, unit-test, actingAs]
layer: 4
---
# Testing

> Feature tests for HTTP, unit tests for Actions — real database always

---

RULE: Feature tests for HTTP endpoints — full request/response cycle
RULE: Unit tests for Action/Service classes
RULE: Real database with `RefreshDatabase` trait — not mocks
RULE: Factories for test data setup
RULE: Test state transitions explicitly

```php
// Feature test — full HTTP cycle
final class ArticleIngestTest extends TestCase
{
    use RefreshDatabase;

    public function test_store_creates_article_with_draft_state(): void
    {
        $domain = Domain::factory()->create();
        $user = User::factory()->create();

        $response = $this->actingAs($user, 'sanctum')
            ->postJson('/api/articles', [
                'title' => 'Test Article',
                'slug' => 'test-article',
                'body' => '# Hello',
                'domain_id' => $domain->id,
                'locale' => 'en',
            ]);

        $response->assertStatus(201);
        $this->assertDatabaseHas('articles', [
            'slug' => 'test-article',
            'state' => ArticleState::Draft->value,
        ]);
    }
}

// Unit test — Action logic
final class PublishArticleActionTest extends TestCase
{
    use RefreshDatabase;

    public function test_publish_transitions_draft_to_published(): void
    {
        $article = Article::factory()->draft()->create();
        $action = new PublishArticleAction();

        $result = $action->execute($article);

        $this->assertEquals(ArticleState::Published, $result->state);
        $this->assertNotNull($result->published_at);
    }

    public function test_publish_rejects_already_published(): void
    {
        $article = Article::factory()->published()->create();
        $action = new PublishArticleAction();

        $this->expectException(InvalidStateTransitionException::class);
        $action->execute($article);
    }
}
```

BANNED: Mocking Eloquent models or database layer
BANNED: Tests that depend on execution order
