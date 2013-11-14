Title: Amazon AppStream as a gamming platform
Date: 2013-11-14
Tags: aws

Amazon just released [AppStream](http://aws.amazon.com/appstream/). The basic idea is that you create a visual app that runs on servers in Amazon's infrastructure and AppStream encodes its video output and streams it to devices such as tablets, smartphones, and desktops. Touches, taps, and swipes on these devices get sent back to your AppStream app so that it can respond to user input. It's like watching a streaming movie where you can control the actors via your TV remote. It's an interesting concept and not unlike how [OnLive](http://www.onlive.com/) works for traditional games.

What differentiates AppStream from OnLive is that instead of turning apps designed for desktops and tablets into video streams, you create an app that takes advantage of AppStream's platform. If the app is designed for this platform then you can do new and interesting things.


The AppStream approach has some advantages:

- Write the bulk of the game once and be able to play it on many different types of devices
- Create stunning real-time visuals that most devices don't have the power to do
- Users never have access to your AppStream app's code or assets so it can't be directly copied or backwards engineered
- You can instantly update your app for all users just by deploying to AppStream
- Instead of having your users download gigs of videos, images, and sounds they only have to download a small client app
- Add new levels and assets to your game without the user having to download anything 

And some disadvantages:

- Users have to be online to play
- The quality of video users recieve is based on their bandwidth
- More latency between when a user taps the screen and when they see the action visualized

Amazon does [mention](http://aws.amazon.com/appstream/faqs/) that you shouldn't use it for highly responsive apps like first person shooters, fighting games, or driving games. It would probably work fine for low interaction games like Candy Crush, Words with Friends, or Tiny Towers. You can also do hybrid games where highly interactive parts are done on the device while computationaly expensive parts are done on AppStream. Doing this though loses some of the advantages of the platform since you still have to write a bunch of code for each device OS you want to deploy to.

I think there might be a sweet spot where AppStream will shine. The MMO. Massive Multiplayer Online games are hybrid apps as it is. Each connected device send user input to the server. The server then figures out where everyone is, what they're trying to do, and what they've already done. It then sends this state information to all connected devices for rendering. This means the device has to have all assets in order to render. If you want the game to look amazing, the device also has to have decent rendering power. Additionally, bandwidth affects how many users can connect and how much information you can share with other users.

With AppStream you can have all devices send their input to a central location, have the app calculate the game state, render the viewpoint of each device, then stream the view to each device. Instead of each device having to have rendering assets and a bandwidth stream of game state, they only need bandwidth to stream a single video stream. The question is: will the bandwidth requirements of the video stream be less than that of the game state stream? Furthermore, could you have more connected devices because of this?

For example, a video stream of 800Kbps would be high quality for an iPhone. With that data stream the device could support an infinite amount of game information because it's all rendered on the server. No matter how much game information there is, only a single video stream is needed. Of course the server's capabilities will limit how much game information there can be, but it's certainly more than a single mobile device can manage. How large is the data stream for a traditional MMO? I imagine it's currently less than 800Kbps because the developers have to balanace between how much information the server can send, how responsive the game is, and how much the device can handle with its CPU, GPU, and memory. 

If all your players had to worry about was having a decent bandwidth connection and you had the powerful infrastrucre of AWS, how many players could you have playing at the same time? Could you take on a 100 zombie horde controlled by real people? Could 1,000 people play a giant game of "king of the hill" at the same time? Could you reproduce a civil war battle with 10,000 soldiers?
