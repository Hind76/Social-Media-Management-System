import heapq  # Import heapq module for implementing max heap

class Post:
    def __init__(self, datetime, post, person, views, comments=None, likes=None):
        # Initialize attributes for the post
        self.datetime = datetime  # Unique datetime value for the post
        self.post = post  # Content of the post
        self.person = person  # Person who posted the content
        self.views = views  # Number of views for the post
        self.comments = comments if comments else []  # List to store comments on the post
        self.likes = likes if likes else 0  # Number of likes on the post

    def add_comment(self, comment):
        # Method to add a comment to the post
        self.comments.append(comment)

    def increment_likes(self):
        # Method to increment the number of likes on the post
        self.likes += 1

class SocialMediaManager:
    def __init__(self):
        # Initialize the social media manager with empty lists and data structures
        self.posts = []  # List to store all posts
        self.post_hash_table = {}  # Hash table for fast lookup by datetime
        self.post_bst = None  # Binary search tree for range queries by datetime
        self.max_heap = MaxHeap()  # Max heap to find the most viewed post

    def add_post(self, post):
        # Method to add a post to the social media manager
        self.posts.append(post)  # Add post to the list of all posts
        self.post_hash_table[post.datetime] = post  # Add post to the hash table for datetime lookup
        if not self.post_bst:
            self.post_bst = BST(post)  # If BST is not initialized, create it with the post as root
        else:
            self.post_bst.insert(post)  # Otherwise, insert the post into the BST
        self.max_heap.insert(post)  # Insert the post into the max heap

    def print_for_you_page(self):
        # Method to print all posts in a format resembling a "For You" page
        print("For You Page:")
        for i, post in enumerate(self.posts):
            print(f"\nPost {i+1}:")  # Print post number
            print(f"DateTime: {post.datetime}")  # Print datetime of the post
            print(f"Post: {post.post}")  # Print the post content
            print(f"Person: {post.person}")  # Print the person who posted it
            print(f"Views: {post.views}")  # Print the number of views
            print(f"Likes: {post.likes}")  # Print the number of likes
            print(f"Comments: {post.comments}")  # Print the comments on the post

    def find_post_by_datetime(self, datetime):
        # Method to find a post by its datetime
        return self.post_hash_table.get(datetime)  # Lookup post in the hash table

    def find_posts_in_range(self, start_datetime, end_datetime):
        # Method to find posts in a specific time range
        if not self.post_bst:
            return []  # Return empty list if BST is not initialized
        return self.post_bst.get_posts_in_range(start_datetime, end_datetime)  # Use BST to find posts in range

    def get_most_viewed_post(self):
        # Method to get the most viewed post
        return self.max_heap.get_most_viewed_post()  # Get the top post from the max heap

    def get_most_liked_post(self):
        # Method to get the most liked post
        most_liked_post = max(self.posts, key=lambda post: post.likes, default=None)  # Find the post with the most likes
        return most_liked_post

class BST:
    def __init__(self, post=None):
        # Initialize the binary search tree with optional root post
        self.root = None
        if post:
            self.root = TreeNode(post)

    def insert(self, post):
        # Method to insert a post into the binary search tree
        if not self.root:
            self.root = TreeNode(post)  # If tree is empty, set post as root
        else:
            self._insert_helper(self.root, post)  # Otherwise, insert recursively

    def _insert_helper(self, node, post):
        # Helper method for inserting a post into the binary search tree
        if post.datetime < node.post.datetime:
            if not node.left:
                node.left = TreeNode(post)  # If left child is None, insert post as left child
            else:
                self._insert_helper(node.left, post)  # Otherwise, recursively insert into left subtree
        else:
            if not node.right:
                node.right = TreeNode(post)  # If right child is None, insert post as right child
            else:
                self._insert_helper(node.right, post)  # Otherwise, recursively insert into right subtree

    def get_posts_in_range(self, start_datetime, end_datetime):
        # Method to get posts within a specific time range
        posts = []  # Initialize list to store posts in range
        self._get_posts_in_range_helper(self.root, start_datetime, end_datetime, posts)  # Start recursive traversal
        return posts

    def _get_posts_in_range_helper(self, node, start_datetime, end_datetime, posts):
        # Helper method to traverse the binary search tree and find posts within a time range
        if not node:
            return  # If node is None, return
        if start_datetime <= node.post.datetime <= end_datetime:
            posts.append(node.post)  # If node's datetime is within range, add post to the list
        if start_datetime < node.post.datetime:
            self._get_posts_in_range_helper(node.left, start_datetime, end_datetime, posts)  # Recursively search left subtree
        if node.post.datetime < end_datetime:
            self._get_posts_in_range_helper(node.right, start_datetime, end_datetime, posts)  # Recursively search right subtree

class TreeNode:
    def __init__(self, post):
        # Initialize a tree node with a post
        self.post = post
        self.left = None
        self.right = None

class MaxHeap:
    def __init__(self):
        # Initialize a max heap to store posts based on views
        self.heap = []

    def insert(self, post):
        # Method to insert a post into the max heap
        heapq.heappush(self.heap, (-post.views, post))  # Insert post into the heap based on views

    def get_most_viewed_post(self):
        # Method to get the most viewed post from the max heap
        return heapq.heappop(self.heap)[1] if self.heap else None  # Pop and return the top post if heap is not empty

# Example usage
if __name__ == "__main__":
    social_media_manager = SocialMediaManager()

    # Adding posts
    post1 = Post(datetime="2024-04-20 12:00:00", post="Hello world!", person="Alice", views=100, likes=10, comments=["Great post!", "Keep it up!"])
    post2 = Post(datetime="2024-04-21 10:00:00", post="Good morning!", person="Bob", views=200, likes=20, comments=["Good day!", "Nice weather!"])
    post3 = Post(datetime="2024-04-22 08:00:00", post="Happy Friday!", person="Alice", views=150, likes=15, comments=["TGIF!", "Enjoy your weekend!"])
    post4 = Post(datetime="2024-04-23 15:00:00", post="Just chilling!", person="Carol", views=180, likes=18, comments=["Relaxing day!", "Love this weather!"])
    post5 = Post(datetime="2024-04-24 09:00:00", post="Sunday brunch!", person="Dave", views=220, likes=22, comments=["Brunch with friends!", "Yummy food!"])
    social_media_manager.add_post(post1)
    social_media_manager.add_post(post2)
    social_media_manager.add_post(post3)
    social_media_manager.add_post(post4)
    social_media_manager.add_post(post5)

    # Print for you page
    social_media_manager.print_for_you_page()

    # Find post by datetime
    found_post = social_media_manager.find_post_by_datetime("2024-04-21 10:00:00")
    print("\nPost found by datetime:", found_post.post if found_post else "Not found")

    # Find posts in a specific time range
    posts_in_range = social_media_manager.find_posts_in_range("2024-04-20 00:00:00", "2024-04-21 23:59:59")
    print("\nPosts found in range:")
    for post in posts_in_range:
        print(f"\nDateTime: {post.datetime}")
        print(f"Post: {post.post}")
        print(f"Person: {post.person}")
        print(f"Views: {post.views}")
        print(f"Likes: {post.likes}")
        print(f"Comments: {post.comments}")

    # Get most viewed post
    most_viewed_post = social_media_manager.get_most_viewed_post()
    print("\nMost viewed post:")
    print(f"\nDateTime: {most_viewed_post.datetime}")
    print(f"Post: {most_viewed_post.post}")
    print(f"Person: {most_viewed_post.person}")
    print(f"Views: {most_viewed_post.views}")
    print(f"Likes: {most_viewed_post.likes}")
    print(f"Comments: {most_viewed_post.comments}")

    # Get most liked post
    most_liked_post = social_media_manager.get_most_liked_post()
    print("\nMost liked post:")
    print(f"\nDateTime: {most_liked_post.datetime}")
    print(f"Post: {most_liked_post.post}")
    print(f"Person: {most_liked_post.person}")
    print(f"Views: {most_liked_post.views}")
    print(f"Likes: {most_liked_post.likes}")
    print(f"Comments: {most_liked_post.comments}" if most_liked_post else "None")
