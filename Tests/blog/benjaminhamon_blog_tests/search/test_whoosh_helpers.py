""" Unit tests for whoosh_helpers """

from benjaminhamon_blog.search import whoosh_helpers


def test_convert_keywords_for_search():
    keyword_collection = [ "MyCategory::MyTag", "MyCategory::AnotherTag", "MyCategory::Subcategory::SomeOtherTag" ]
    searchable_values = whoosh_helpers.convert_keywords_for_search(keyword_collection)
    expected_values = keyword_collection + [ "MyCategory", "MyTag", "AnotherTag", "Subcategory", "SomeOtherTag" ]

    assert searchable_values == " ".join(sorted(expected_values))
